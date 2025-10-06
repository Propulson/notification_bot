from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_keyboard():
    """Inline клавиатура прикрепленная к сообщению"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Наш сайт", url="https://example.com")],
            [InlineKeyboardButton(text="📱 Канал", url="https://t.me/example")],
            [InlineKeyboardButton(text="⭐️ Рейтинг", callback_data="rating")],
            [InlineKeyboardButton(text="🔔 Подписаться", callback_data="subscribe")],
            [InlineKeyboardButton(text="📞 Связаться", callback_data="contact")]
        ]
    )
    return keyboard

def get_inline_actions():
    """Inline клавиатура для действий"""
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
    """Inline клавиатура для админских действий"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Выдать админку", callback_data="admin_grant"),
             InlineKeyboardButton(text="❌ Забрать админку", callback_data="admin_revoke")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")]
        ]
    )
    return keyboard