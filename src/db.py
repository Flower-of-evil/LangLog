import sqlite3
from pathlib import Path
from . import config

DB_PATH = config.get_db_path()

def init_db():
    """Создаёт таблицы, если их нет"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS languages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                level TEXT CHECK(level IN ('A1','A2','B1','B2','C1','C2')),
                goal TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS practice_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                duration_min INTEGER NOT NULL,
                activity_type TEXT CHECK(activity_type IN (
                    'чтение','письмо','аудирование','говорение','грамматика','словарный запас'
                )),
                materials TEXT,
                effectiveness_rating INTEGER CHECK(effectiveness_rating BETWEEN 1 AND 10),
                FOREIGN KEY(language_id) REFERENCES languages(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()

def get_all_languages():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM languages ORDER BY id").fetchall()
        return [dict(row) for row in rows]

def add_language(name, level, goal):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO languages (name, level, goal) VALUES (?, ?, ?)",
            (name, level, goal)
        )
        conn.commit()
        return cursor.lastrowid

def add_session(lang_id, date, duration, act_type, materials, rating):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            '''INSERT INTO practice_sessions
               (language_id, date, duration_min, activity_type, materials, effectiveness_rating)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (lang_id, date, duration, act_type, materials, rating)
        )
        conn.commit()
        return cursor.lastrowid

def get_sessions_by_language(lang_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM practice_sessions WHERE language_id = ? ORDER BY date",
            (lang_id,)
        ).fetchall()
        return [dict(row) for row in rows]