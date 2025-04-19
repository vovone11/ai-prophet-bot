
import sqlite3
from config import DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                user_id INTEGER,
                q1 INTEGER,
                q2 INTEGER,
                q3 INTEGER
            )
        """)
        conn.commit()

def save_answers(user_id, answers):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO answers (user_id, q1, q2, q3) VALUES (?, ?, ?, ?)",
                  (user_id, *answers))
        conn.commit()
