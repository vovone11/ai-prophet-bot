import sqlite3

def create_db():
    # Создаем подключение к базе данных
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Создаем таблицу, если она еще не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        age TEXT,
                        gender TEXT,
                        job TEXT,
                        routine TEXT,
                        lifestyle TEXT,
                        health TEXT,
                        food TEXT,
                        goals TEXT,
                        social TEXT)''')

    conn.commit()
    conn.close()

def save_user_data(user_data):
    # Подключаемся к базе данных
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Вставляем данные пользователя в таблицу
    cursor.execute('''INSERT INTO user_data (age, gender, job, routine, lifestyle, health, food, goals, social) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (user_data['age'], user_data['gender'], user_data['job'], user_data['routine'], 
                       user_data['lifestyle'], user_data['health'], user_data['food'], user_data['goals'], 
                       user_data['social']))

    conn.commit()
    conn.close()

def get_all_users():
    # Получаем все данные пользователей
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data")
    users = cursor.fetchall()

    conn.close()

    return users