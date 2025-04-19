import openai
from django.shortcuts import render
from django.http import JsonResponse
import os
import logging

# Configurez votre clé API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

logger = logging.getLogger(__name__)

def chat_view(request):
    return render(request, 'chatbot/chat.html')

def send_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        try:
            # Utilisez le modèle gpt-3.5-turbo
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant AI."},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=150
            )
            ai_response = response['choices'][0]['message']['content'].strip()
            return JsonResponse({'message': user_message, 'response': ai_response})
        except Exception as e:
            logger.error(f"Erreur lors de l'appel à l'API OpenAI : {e}")
            return JsonResponse({'error': f"Erreur lors de l'appel à l'API OpenAI : {e}"}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)