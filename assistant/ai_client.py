import os
import requests

def ask_ai(message: str, history: list[dict] | None = None) -> str:
    url = os.environ.get('AI_API_URL')
    model = os.environ.get('AI_MODEL', 'llama3.2')
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': 'Ты — дружелюбный ИИ-ассистент дневника домашних питомцев. Отвечай кратко и по-русски.'},
            *(history or []),
            {'role': 'user', 'content': message},
        ],
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']