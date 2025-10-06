import sqlite3
import os
from datetime import datetime

# Путь к базе данных
DB_PATH = "database/bot.db"


def init_db():
    """Инициализация базы данных"""
    # Создаем папку если её нет
    os.makedirs('database', exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            is_active BOOLEAN DEFAULT 1,
            is_admin BOOLEAN DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_activity TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Таблица администраторов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            permissions TEXT DEFAULT 'basic',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")


def get_db():
    """Получить соединение с базой данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Чтобы получать результаты как словари
    return conn