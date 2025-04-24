def build_prompt(data):
    # Проверяем, что все ключи присутствуют в данных
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

    Сделай 3 сценария будущего (если ничего не менять, если немного улучшить, если всё усугубится). В каждом — краткий заголовок, описание и советы.
    """