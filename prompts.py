def build_prompt(answers):
    prompt = "На основе следующих данных о человеке спрогнозируй его будущее:\n"
    for key, value in answers.items():
        prompt += f"{key}: {value}\n"
    prompt += "\nПредсказание:"
    return prompt