from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import openai
from .models import ChatMessage
from django.conf import settings

# Create your views here.

# @login_required
def chat_view(request):
    # messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:10]
    messages = [{"message": "Bienvenue !", "response": "Comment puis-je vous aider ?"}]
    return render(request, 'chatbot/chat.html', {'messages': messages})

# @login_required
# @require_POST
# @csrf_exempt
def send_message(request):
    message = request.POST.get('message')
    print(message)
    if not message:
        return JsonResponse({'error': 'Message vide'}, status=400)
    
    try:
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant pédagogique qui aide les étudiants dans leur apprentissage."},
                {"role": "user", "content": message}
            ]
        )
        
        ai_response = response.choices[0].message.content
        
        # Sauvegarder le message et la réponse
        ChatMessage.objects.create(
            user=request.user,
            message=message,
            response=ai_response
        )
        
        return JsonResponse({'response': ai_response})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
