import sqlite3
import datetime

DB_NAME = 'english_bot.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Таблица пользователей
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Таблица слов пользователя
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            example TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            times_asked INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            last_asked TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name))
    conn.commit()
    conn.close()

def add_word(user_id, word, translation, example=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO user_words (user_id, word, translation, example)
        VALUES (?, ?, ?, ?)
    ''', (user_id, word, translation, example))
    conn.commit()
    conn.close()

def get_user_words(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT word, translation, example FROM user_words WHERE user_id=?
    ''', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_random_word(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT id, word, translation FROM user_words WHERE user_id=?
        ORDER BY RANDOM() LIMIT 1
    ''', (user_id,))
    row = cur.fetchone()
    conn.close()
    return row  # (id, word, translation)

def update_stat(word_id, correct):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        UPDATE user_words
        SET times_asked = times_asked + 1,
            correct_answers = correct_answers + ?,
            last_asked = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (1 if correct else 0, word_id))
    conn.commit()
    conn.close()

def word_exists(user_id, word):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT 1 FROM user_words WHERE user_id=? AND word=?
    ''', (user_id, word))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def delete_word(user_id, word):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM user_words WHERE user_id=? AND word=?
    ''', (user_id, word))
    conn.commit()
    conn.close()
