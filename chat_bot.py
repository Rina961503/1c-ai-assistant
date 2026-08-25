import json
import requests

while True:
    q = input('>>> ')
    if q.lower() in ('exit', 'quit', 'пока'):
        break
    try:
        r = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': 'qwen3:8b', 'prompt': q, 'stream': True},
            timeout=600,
            stream=True
        )
        for line in r.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode('utf-8'))
            if 'error' in data:
                print('\nОшибка сервера:', data['error'])
                break
            print(data.get('response', ''), end='', flush=True)
        print()
    except requests.exceptions.ConnectionError:
        print('Не могу подключиться к Ollama. Проверь: systemctl status ollama')
    except requests.exceptions.Timeout:
        print('Модель думала слишком долго. Попробуй вопрос попроще.')
    except Exception as e:
        print('Что-то пошло не так:', e)
