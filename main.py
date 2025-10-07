import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ⚠️ ЗАМЕНИТЕ ЭТОТ ТОКЕН НА ВАШ РЕАЛЬНЫЙ ТОКЕН!
BOT_TOKEN = "8285963956:AAECt8ixerW0PqRwDLyilxc0EQsvyzBszZQ"

# Проверка токена перед запуском
if not BOT_TOKEN or ":" not in BOT_TOKEN:
    print("❌ ОШИБКА: Неверный токен!")
    print("📝 Получите токен у @BotFather командой /newbot")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== ОБЫЧНАЯ REPLY-КЛАВИАТУРА ==========
def get_main_keyboard():
    """Основная клавиатура внизу экрана"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="ℹ️ Помощь")],
            [KeyboardButton(text="🎯 Инлайн меню")]
        ],
        resize_keyboard=True,  # Клавиатура подстраивается под размер экрана
        one_time_keyboard=False  # Клавиатура не скрывается после нажатия
    )
    return keyboard

def get_settings_keyboard():
    """Клавиатура для настроек"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔔 Уведомления"), KeyboardButton(text="🌐 Язык")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )
    return keyboard

# ========== INLINE-КЛАВИАТУРА ==========
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

# ========== ОБРАБОТЧИКИ КОМАНД ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "🎉 Добро пожаловать!\n\n"
        "Я ваш телеграм бот с клавиатурами!\n"
        "Используйте кнопки ниже или команды."
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "📚 <b>Доступные команды:</b>\n\n"
        "/start - Запустить бота\n"
        "/help - Помощь\n"
        "/inline - Показать инлайн меню\n"
        "/keyboard - Показать основную клавиатуру\n\n"
        "<b>Или используйте кнопки:</b>"
    )
    await message.answer(help_text, parse_mode="HTML", reply_markup=get_main_keyboard())

@dp.message(Command("inline"))
async def cmd_inline(message: types.Message):
    await message.answer("🔘 Выберите действие:", reply_markup=get_inline_keyboard())

@dp.message(Command("keyboard"))
async def cmd_keyboard(message: types.Message):
    await message.answer("⌨️ Основное меню:", reply_markup=get_main_keyboard())

# ========== ОБРАБОТЧИКИ КНОПОК REPLY-КЛАВИАТУРЫ ==========
@dp.message(lambda message: message.text == "📊 Статистика")
async def handle_statistics(message: types.Message):
    await message.answer("📈 <b>Статистика:</b>\n\n• Пользователей: 1\n• Сообщений: 10\n• Активность: высокая",
                        parse_mode="HTML")

@dp.message(lambda message: message.text == "⚙️ Настройки")
async def handle_settings(message: types.Message):
    await message.answer("⚙️ <b>Настройки:</b>\n\nВыберите раздел:",
                        parse_mode="HTML",
                        reply_markup=get_settings_keyboard())

@dp.message(lambda message: message.text == "📞 Контакты")
async def handle_contacts(message: types.Message):
    contact_text = (
        "📞 <b>Контакты:</b>\n\n"
        "🌐 Сайт: example.com\n"
        "📧 Email: info@example.com\n"
        "📱 Телеграм: @username"
    )
    await message.answer(contact_text, parse_mode="HTML")

@dp.message(lambda message: message.text == "ℹ️ Помощь")
async def handle_help(message: types.Message):
    await cmd_help(message)

@dp.message(lambda message: message.text == "🎯 Инлайн меню")
async def handle_inline_menu(message: types.Message):
    await cmd_inline(message)

@dp.message(lambda message: message.text == "🔙 Назад")
async def handle_back(message: types.Message):
    await message.answer("↩️ Возврат в главное меню:", reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "🔔 Уведомления")
async def handle_notifications(message: types.Message):
    await message.answer("🔔 <b>Настройки уведомлений:</b>\n\nВсе уведомления включены ✅",
                        parse_mode="HTML")

@dp.message(lambda message: message.text == "🌐 Язык")
async def handle_language(message: types.Message):
    await message.answer("🌐 <b>Выбор языка:</b>\n\nТекущий язык: Русский 🇷🇺",
                        parse_mode="HTML")

# ========== ОБРАБОТЧИКИ INLINE-КНОПОК ==========
@dp.callback_query(lambda callback: callback.data == "rating")
async def handle_rating_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("⭐️ <b>Ваш рейтинг:</b> 5.0\n\nСпасибо за использование бота!",
                                   parse_mode="HTML")

@dp.callback_query(lambda callback: callback.data == "subscribe")
async def handle_subscribe_callback(callback: types.CallbackQuery):
    await callback.answer("✅ Вы подписались на обновления!", show_alert=True)

@dp.callback_query(lambda callback: callback.data == "contact")
async def handle_contact_callback(callback: types.CallbackQuery):
    await callback.message.answer("📞 Для связи: @username")

@dp.callback_query(lambda callback: callback.data == "confirm")
async def handle_confirm_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("✅ Действие подтверждено!",
                                   reply_markup=get_inline_actions())

@dp.callback_query(lambda callback: callback.data == "cancel")
async def handle_cancel_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("❌ Действие отменено!",
                                   reply_markup=get_inline_actions())

@dp.callback_query(lambda callback: callback.data == "refresh")
async def handle_refresh_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("🔄 Данные обновлены!\n\nТекущее время: ...",
                                   reply_markup=get_inline_actions())

@dp.callback_query(lambda callback: callback.data == "settings")
async def handle_settings_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("⚙️ <b>Настройки:</b>\n\nИспользуйте команду /keyboard для основных настроек",
                                   parse_mode="HTML",
                                   reply_markup=get_inline_actions())

# ========== ОБРАБОТЧИК ЛЮБЫХ СООБЩЕНИЙ ==========
@dp.message()
async def handle_any_message(message: types.Message):
    await message.answer("🤖 Используйте кнопки или команды для взаимодействия с ботом!\n\n"
                        "Команда /help - список всех возможностей",
                        reply_markup=get_main_keyboard())

async def main():
    print("🤖 Запуск бота...")
    print(f"✅ Токен: {BOT_TOKEN[:10]}...")  # Показываем только начало токена
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())