import json
import os
import urllib.error
import urllib.request

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from pets.models import Pet
from .models import Conversation, Message


def _ask_model(messages):
    api_key = os.environ.get('AI_PROVIDER_API_KEY', '')
    endpoint = os.environ.get('AI_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
    model = os.environ.get('AI_MODEL', 'openai/gpt-4o-mini')
    if not api_key:
        raise RuntimeError('ИИ-помощник не настроен: добавьте AI_PROVIDER_API_KEY в .env.')
    payload = json.dumps({'model': model, 'messages': messages, 'temperature': 0.4}).encode()
    request = urllib.request.Request(endpoint, data=payload, headers={
        'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost', 'X-Title': 'PetDiary',
    }, method='POST')
    with urllib.request.urlopen(request, timeout=45) as response:
        result = json.loads(response.read().decode())
    return result['choices'][0]['message']['content'].strip()


@login_required
@require_http_methods(['GET', 'POST'])
def assistant_chat(request):
    if request.method == 'GET':
        conversations = Conversation.objects.filter(user=request.user)
        conversation_id = request.GET.get('conversation')
        if conversation_id:
            conversation = get_object_or_404(conversations, pk=conversation_id)
        else:
            conversation = conversations.first()
        if conversation is None:
            conversation = Conversation.objects.create(user=request.user)
        return render(request, 'assistant/chat.html', {
            'conversation': conversation,
            'messages': conversation.messages.all(),
            'conversations': conversations,
        })

    try:
        data = json.loads(request.body or '{}')
        prompt = str(data.get('message', '')).strip()
        conversation_id = data.get('conversation')
        if not prompt or len(prompt) > 4000:
            return JsonResponse({'error': 'Введите сообщение длиной до 4000 символов.'}, status=400)
        conversations = Conversation.objects.filter(user=request.user)
        conversation = get_object_or_404(conversations, pk=conversation_id) if conversation_id else Conversation.objects.create(user=request.user)
        Message.objects.create(conversation=conversation, role='user', content=prompt)

        pet_context = list(Pet.objects.filter(owner=request.user).values('name', 'species', 'breed', 'weight')[:20])
        history = list(conversation.messages.order_by('-created_at').values('role', 'content')[:12])
        history.reverse()
        system_prompt = (
            'Ты — помощник приложения PetDiary. Отвечай по-русски, доброжелательно и кратко. '
            'Помогай вести дневник и планировать уход за питомцами. Не ставь диагнозы и не назначай лечение; '
            'при тревожных симптомах рекомендуй обратиться к ветеринару. '
            f'Контекст питомцев текущего пользователя (данные приватны): {json.dumps(pet_context, ensure_ascii=False, default=str)}'
        )
        answer = _ask_model([{'role': 'system', 'content': system_prompt}] + history)
        Message.objects.create(conversation=conversation, role='assistant', content=answer)
        conversation.save(update_fields=['updated_at'])
        return JsonResponse({'answer': answer, 'conversation': conversation.pk})
    except RuntimeError as exc:
        return JsonResponse({'error': str(exc)}, status=503)
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as exc:
        return JsonResponse({'error': 'Не удалось получить ответ ИИ. Проверьте настройки провайдера и повторите попытку.'}, status=502)
