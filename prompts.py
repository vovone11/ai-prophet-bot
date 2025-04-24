import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def build_prompt(data):
    required_keys = ['age', 'gender', 'job', 'routine', 'lifestyle', 'health', 'food', 'goals', 'social']
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Отсутствуют данные для: {', '.join(missing_keys)}")

    return f"""
    Ты — ИИ-прорицатель. Проанализируй образ жизни человека и предскажи его будущее.

    Вот его данные:
    Возраст: {data['age']}
    Пол: {data['gender']}
    Профессия: {data['job']}
    Распорядок дня: {data['routine']}
    Образ жизни: {data['lifestyle']}
    Здоровье: {data['health']}
    Питание: {data['food']}
    Цели: {data['goals']}
    Социальные связи: {data['social']}

    Сделай 3 сценария будущего (если ничего не менять, если немного улучшить, если всё усугубится).
    Для каждого сценария:
    - Заголовок
    - Краткое описание
    - Советы
    """


def generate_forecast(data):
    prompt = build_prompt(data)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=700
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        print(f"Ошибка при обращении к OpenAI: {e}")
        return "Произошла ошибка при генерации прогноза. Попробуй позже."