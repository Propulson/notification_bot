from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import get_admin_keyboard, get_main_keyboard
from keyboards.inline import get_admin_actions
from utils.users import get_all_users, get_users_count, grant_admin, revoke_admin, is_admin, get_active_users_count, \
    get_all_admins

router = Router()


class BroadcastState(StatesGroup):
    waiting_for_message = State()


class AdminGrantState(StatesGroup):
    waiting_for_user_id = State()


class AdminRevokeState(StatesGroup):
    waiting_for_user_id = State()


# Команда админки - ДУБЛИРУЕМ для надежности
@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    print(f"🔍 Обработчик /admin для пользователя {message.from_user.id}")

    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        return

    admin_text = (
        "👑 <b>Панель администратора</b>\n\n"
        "Доступные команды:\n"
        "• /admin - панель администратора\n"
        "• /stats - статистика бота\n"
        "• /broadcast - рассылка сообщений\n"
        "• /users - список пользователей\n\n"
        "Или используйте кнопки ниже:"
    )
    await message.answer(admin_text, parse_mode="HTML", reply_markup=get_admin_keyboard())


# Статистика - ДУБЛИРУЕМ команду
@router.message(Command("stats"))
async def cmd_stats_command(message: types.Message):
    print(f"📊 Обработчик /stats для пользователя {message.from_user.id}")
    await cmd_stats(message)


# Статистика по кнопке
async def cmd_stats(message: types.Message):
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        return

    users_count = await get_users_count()
    active_users = await get_active_users_count(7)

    stats_text = (
        "📊 <b>Статистика бота</b>\n\n"
        f"👥 Всего пользователей: <b>{users_count}</b>\n"
        f"🟢 Активных за неделю: <b>{active_users}</b>\n"
        f"📈 Охват: <b>{(active_users / users_count * 100 if users_count > 0 else 0):.1f}%</b>"
    )
    await message.answer(stats_text, parse_mode="HTML")


# Пользователи - ДУБЛИРУЕМ команду
@router.message(Command("users"))
async def cmd_users_command(message: types.Message):
    print(f"👥 Обработчик /users для пользователя {message.from_user.id}")
    await cmd_users(message)


# Пользователи по кнопке
async def cmd_users(message: types.Message):
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        return

    users = await get_all_users()
    users_text = "👥 <b>Последние 10 пользователей:</b>\n\n"

    if not users:
        users_text = "👥 <b>Пользователи:</b>\n\nПока нет зарегистрированных пользователей."
    else:
        for user in users[:10]:
            users_text += f"• ID: {user.user_id}\n"
            if user.username:
                users_text += f"  @{user.username}\n"
            if user.first_name:
                users_text += f"  {user.first_name}"
                if user.last_name:
                    users_text += f" {user.last_name}"
                users_text += "\n"
            users_text += f"  📅 {user.created_at[:10]}\n\n"

    await message.answer(users_text, parse_mode="HTML", reply_markup=get_admin_actions())


# Рассылка - ДУБЛИРУЕМ команду
@router.message(Command("broadcast"))
async def cmd_broadcast_command(message: types.Message, state: FSMContext):
    print(f"📢 Обработчик /broadcast для пользователя {message.from_user.id}")
    await cmd_broadcast(message, state)


# Рассылка по кнопке
async def cmd_broadcast(message: types.Message, state: FSMContext = None):
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        return

    await message.answer(
        "📢 <b>Рассылка сообщений</b>\n\n"
        "Отправьте сообщение которое хотите разослать всем пользователям.\n"
        "Можно использовать HTML разметку.",
        parse_mode="HTML"
    )
    if state:
        await state.set_state(BroadcastState.waiting_for_message)


# Управление админами по кнопке
async def cmd_admins(message: types.Message):
    print(f"👑 Обработчик кнопки Админы для пользователя {message.from_user.id}")

    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        return

    admins = await get_all_admins()

    admins_text = "👑 <b>Список администраторов:</b>\n\n"
    if not admins:
        admins_text = "👑 <b>Администраторы:</b>\n\nНет зарегистрированных администраторов."
    else:
        for admin in admins:
            admins_text += f"• ID: {admin.user_id}\n"
            if admin.username:
                admins_text += f"  @{admin.username}\n"
            admins_text += f"  📅 {admin.created_at[:10]}\n\n"

    await message.answer(admins_text, parse_mode="HTML", reply_markup=get_admin_actions())


# Обработка сообщения для рассылки
@router.message(BroadcastState.waiting_for_message)
async def process_broadcast_message(message: types.Message, state: FSMContext, bot):
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        await state.clear()
        return

    users = await get_all_users()
    success_count = 0
    fail_count = 0

    progress_msg = await message.answer("🔄 Начинаю рассылку...")

    for user in users:
        try:
            await bot.send_message(
                chat_id=user.user_id,
                text=message.text,
                parse_mode="HTML" if message.html_text else None
            )
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"Ошибка отправки пользователю {user.user_id}: {e}")

    result_text = (
        "✅ <b>Рассылка завершена!</b>\n\n"
        f"📨 Отправлено: <b>{success_count}</b>\n"
        f"❌ Не отправлено: <b>{fail_count}</b>\n"
        f"📊 Всего пользователей: <b>{len(users)}</b>"
    )
    await progress_msg.edit_text(result_text, parse_mode="HTML")
    await state.clear()


# Inline кнопки админки
@router.callback_query(F.data == "admin_grant")
async def handle_admin_grant(callback: types.CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав!", show_alert=True)
        return

    await callback.message.answer(
        "👑 <b>Выдача прав администратора</b>\n\n"
        "Отправьте ID пользователя которому хотите выдать админку:",
        parse_mode="HTML"
    )
    await state.set_state(AdminGrantState.waiting_for_user_id)
    await callback.answer()


@router.callback_query(F.data == "admin_revoke")
async def handle_admin_revoke(callback: types.CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав!", show_alert=True)
        return

    await callback.message.answer(
        "❌ <b>Забрать права администратора</b>\n\n"
        "Отправьте ID пользователя у которого хотите забрать админку:",
        parse_mode="HTML"
    )
    await state.set_state(AdminRevokeState.waiting_for_user_id)
    await callback.answer()


@router.message(AdminGrantState.waiting_for_user_id)
async def process_admin_grant(message: types.Message, state: FSMContext):
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        await state.clear()
        return

    try:
        user_id = int(message.text)
        success = await grant_admin(user_id, "", message.from_user.id)

        if success:
            await message.answer(f"✅ Пользователю {user_id} выданы права администратора!")
        else:
            await message.answer(f"⚠️ Пользователь {user_id} уже является администратором!")

    except ValueError:
        await message.answer("❌ Неверный формат ID! Отправьте числовой ID.")

    await state.clear()


@router.message(AdminRevokeState.waiting_for_user_id)
async def process_admin_revoke(message: types.Message, state: FSMContext):
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        await state.clear()
        return

    try:
        user_id = int(message.text)
        success = await revoke_admin(user_id)

        if success:
            await message.answer(f"✅ У пользователя {user_id} забраны права администратора!")
        else:
            await message.answer(f"⚠️ Пользователь {user_id} не является администратором!")

    except ValueError:
        await message.answer("❌ Неверный формат ID! Отправьте числовой ID.")

    await state.clear()


# Возврат в главное меню
@router.message(F.text == "🔙 В главное меню")
async def handle_back_to_main(message: types.Message):
    await message.answer("↩️ Возврат в главное меню:", reply_markup=get_main_keyboard())