from datetime import datetime
from database.base import get_db
from database.models import User, Admin


async def get_or_create_user(user_id: int, username: str = None,
                             first_name: str = None, last_name: str = None):
    """Получить или создать пользователя"""
    conn = get_db()
    cursor = conn.cursor()

    # Проверяем существует ли пользователь
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    current_time = datetime.now().isoformat()

    if not user_data:
        # Создаем нового пользователя
        cursor.execute('''
            INSERT INTO users (user_id, username, first_name, last_name, created_at, last_activity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, current_time, current_time))
        conn.commit()
        print(f"✅ Создан новый пользователь: {user_id}")
    else:
        # Обновляем существующего пользователя
        cursor.execute('''
            UPDATE users 
            SET username = ?, first_name = ?, last_name = ?, last_activity = ?
            WHERE user_id = ?
        ''', (username or user_data['username'],
              first_name or user_data['first_name'],
              last_name or user_data['last_name'],
              current_time, user_id))
        conn.commit()
        print(f"✅ Обновлен пользователь: {user_id}")

    # Получаем обновленные данные пользователя
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    return User(**user_data) if user_data else None


async def is_admin(user_id: int):
    """Проверить является ли пользователь администратором"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,))
    admin_data = cursor.fetchone()
    conn.close()

    return admin_data is not None


async def get_all_users():
    """Получить всех пользователей"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY created_at DESC')
    users_data = cursor.fetchall()
    conn.close()

    return [User(**user) for user in users_data]


async def get_users_count():
    """Получить количество пользователей"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_active = 1')
    count = cursor.fetchone()['count']
    conn.close()

    return count


async def grant_admin(user_id: int, username: str, granted_by: int):
    """Выдать права администратора"""
    conn = get_db()
    cursor = conn.cursor()

    # Проверяем не является ли уже админом
    cursor.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,))
    admin_data = cursor.fetchone()

    if not admin_data:
        # Выдаем админку
        cursor.execute('''
            INSERT INTO admins (user_id, username, created_by)
            VALUES (?, ?, ?)
        ''', (user_id, username, granted_by))

        # Обновляем статус в таблице пользователей
        cursor.execute('UPDATE users SET is_admin = 1 WHERE user_id = ?', (user_id,))

        conn.commit()
        conn.close()
        print(f"✅ Выданы админские права пользователю: {user_id}")
        return True

    conn.close()
    print(f"⚠️ Пользователь {user_id} уже является администратором")
    return False


async def revoke_admin(user_id: int):
    """Забрать права администратора"""
    conn = get_db()
    cursor = conn.cursor()

    # Проверяем является ли админом
    cursor.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,))
    admin_data = cursor.fetchone()

    if admin_data:
        # Забираем админку
        cursor.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))

        # Обновляем статус в таблице пользователей
        cursor.execute('UPDATE users SET is_admin = 0 WHERE user_id = ?', (user_id,))

        conn.commit()
        conn.close()
        print(f"✅ Забраны админские права у пользователя: {user_id}")
        return True

    conn.close()
    print(f"⚠️ Пользователь {user_id} не является администратором")
    return False


async def get_active_users_count(days=7):
    """Получить количество активных пользователей за последние N дней"""
    conn = get_db()
    cursor = conn.cursor()

    from datetime import datetime, timedelta
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

    cursor.execute('''
        SELECT COUNT(*) as count FROM users 
        WHERE last_activity > ? AND is_active = 1
    ''', (cutoff_date,))

    count = cursor.fetchone()['count']
    conn.close()

    return count


async def get_all_admins():
    """Получить всех администраторов"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admins ORDER BY created_at DESC')
    admins_data = cursor.fetchall()
    conn.close()

    return [Admin(**admin) for admin in admins_data]