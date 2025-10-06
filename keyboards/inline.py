from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Наш сайт", url="https://example.com")],
            [InlineKeyboardButton(text="📱 Канал", url="https://t.me/example")],
        ]
    )
    return keyboard

def get_inline_actions():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm"),
             InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")],
            [InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh"),
             InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
        ]
    )
    return keyboard

def get_admin_actions():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Выдать админку", callback_data="admin_grant"),
             InlineKeyboardButton(text="❌ Забрать админку", callback_data="admin_revoke")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")]
        ]
    )
    return keyboard