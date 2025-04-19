
def generate_prediction(answers):
    score = sum(answers)
    if score < 5:
        return "Твоя душа спокойна, твой путь ясен."
    elif score < 10:
        return "Ты на перепутье. Прислушайся к себе."
    else:
        return "Ветер перемен уже рядом. Готовься!"
