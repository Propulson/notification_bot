from aiogram import Router, types
from keyboards.reply import get_main_keyboard, get_settings_keyboard
from utils.users import is_admin

router = Router()


@router.message()
async def handle_any_message(message: types.Message):
    print(f"🔍 Получено сообщение: '{message.text}' от пользователя {message.from_user.id}")

    # Проверяем админские права
    admin_status = await is_admin(message.from_user.id)
    print(f"👤 Пользователь {message.from_user.id} админ: {admin_status}")

    # Если пользователь админ и использует админские кнопки
    if admin_status:
        if message.text == "📊 Статистика":
            from handlers.admin import cmd_stats
            await cmd_stats(message)
            return
        elif message.text == "👥 Пользователи":
            from handlers.admin import cmd_users
            await cmd_users(message)
            return
        elif message.text == "📢 Рассылка":
            from handlers.admin import cmd_broadcast
            from aiogram.fsm.context import FSMContext
            # Нужно передать state, но пока просто отправляем сообщение
            await message.answer("📢 <b>Рассылка сообщений</b>\n\nОтправьте сообщение для рассылки.", parse_mode="HTML")
            return
        elif message.text == "👑 Админы":
            from handlers.admin import cmd_admins
            await cmd_admins(message)
            return
        elif message.text == "🔙 В главное меню":
            await message.answer("↩️ Возврат в главное меню:", reply_markup=get_main_keyboard())
            return

    # Обычные кнопки для всех пользователей
    if message.text == "📊 Статистика":
        await message.answer("📊 <b>Базовая статистика:</b>\n\nБот работает стабильно! ✅", parse_mode="HTML")
    elif message.text == "⚙️ Настройки":
        await message.answer("⚙️ <b>Настройки:</b>\n\nВыберите раздел:", parse_mode="HTML",
                             reply_markup=get_settings_keyboard())
    elif message.text == "📞 Контакты":
        contact_text = (
            "📞 <b>Контакты:</b>\n\n"
            "🌐 Сайт: example.com\n"
            "📧 Email: info@example.com\n"
            "📱 Телеграм: @username"
        )
        await message.answer(contact_text, parse_mode="HTML")
    elif message.text == "ℹ️ Помощь":
        from handlers.commands import cmd_help
        await cmd_help(message)
    elif message.text == "🎯 Инлайн меню":
        from handlers.commands import cmd_inline
        await cmd_inline(message)
    elif message.text == "🔙 Назад":
        await message.answer("↩️ Возврат в главное меню:", reply_markup=get_main_keyboard())
    elif message.text == "🔔 Уведомления":
        await message.answer("🔔 <b>Настройки уведомлений:</b>\n\nВсе уведомления включены ✅", parse_mode="HTML")
    elif message.text == "🌐 Язык":
        await message.answer("🌐 <b>Выбор языка:</b>\n\nТекущий язык: Русский 🇷🇺", parse_mode="HTML")
    else:
        await message.answer(
            "🤖 Используйте кнопки или команды для взаимодействия с ботом!\n\n"
            "Команда /help - список всех возможностей",
            reply_markup=get_main_keyboard() if not admin_status else get_main_keyboard()
        )