import json
import requests

SYSTEM_PROMPT = """Ты — эксперт по разработке в 1С:Предприятие 8.3.
Ты помогаешь программисту писать, объяснять и отлаживать код на встроенном языке 1С.

Твои правила:
1. Используй ТОЛЬКО реальные функции и методы платформы 1С:Предприятие 8.3. Никогда не выдумывай функции.
2. Для вывода сообщений используй Сообщить(). Функции "Вывод()" не существует.
3. Запросы к базе пиши на языке запросов 1С: ВЫБРАТЬ ... ИЗ ... ГДЕ ...
4. Отвечай на русском языке. Объясняй подробно и просто, как для начинающего: что делает каждая строчка кода и почему.
5. Если не уверен в ответе — честно скажи об этом.
6. Приводи примеры кода с комментариями.
7. Всегда объясняй, где и как запустить код: какой объект создать в Конфигураторе 1С (обработка, общий модуль, форма), куда вставить код и какую кнопку нажать, чтобы увидеть результат."""

while True:
    q = input('>>> ')
    if q.lower() in ('exit', 'quit', 'пока'):
        break
    try:
        r = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': 'qwen3:8b', 'prompt': q, 'system': SYSTEM_PROMPT, 'stream': True},
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
