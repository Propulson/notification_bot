from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="ℹ️ Помощь")],
            [KeyboardButton(text="🎯 Инлайн меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_settings_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔔 Уведомления"), KeyboardButton(text="🌐 Язык")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="👥 Пользователи")],
            [KeyboardButton(text="📢 Рассылка"), KeyboardButton(text="👑 Админы")],
            [KeyboardButton(text="🔙 В главное меню")]
        ],
        resize_keyboard=True
    )
    return keyboard