import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from django.contrib.auth import get_user_model
import openai
from django.conf import settings

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        
        if user.is_authenticated:
            # Sauvegarder le message
            await self.save_message(user, message)
            
            # Obtenir la réponse de l'IA
            ai_response = await self.get_ai_response(message)
            
            # Sauvegarder la réponse
            await self.save_message(user, ai_response, is_response=True)
            
            # Envoyer le message et la réponse au groupe
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'response': ai_response,
                    'user': user.email
                }
            )
    
    async def chat_message(self, event):
        message = event['message']
        response = event['response']
        user = event['user']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'response': response,
            'user': user
        }))
    
    @database_sync_to_async
    def save_message(self, user, content, is_response=False):
        if is_response:
            ChatMessage.objects.create(
                user=user,
                message="",
                response=content
            )
        else:
            ChatMessage.objects.create(
                user=user,
                message=content,
                response=""
            )
    
    @database_sync_to_async
    def get_ai_response(self, message):
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant pédagogique qui aide les étudiants dans leur apprentissage."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content 