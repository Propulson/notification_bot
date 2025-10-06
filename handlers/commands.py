from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import get_main_keyboard, get_admin_keyboard
from keyboards.inline import get_inline_keyboard
from utils.users import get_or_create_user, is_admin

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Сохраняем/обновляем пользователя в базе
    user = await get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    welcome_text = (
        "🎉 Добро пожаловать!\n\n"
        "Я ваш телеграм бот с клавиатурами и базой данных!\n"
        "Используйте кнопки ниже или команды."
    )

    # Проверяем является ли пользователь админом
    admin_status = await is_admin(message.from_user.id)
    print(f"👤 User {message.from_user.id} admin status: {admin_status}")

    if admin_status:
        await message.answer(welcome_text, reply_markup=get_admin_keyboard())
        await message.answer("👑 <b>Вам доступна панель администратора!</b>\nИспользуйте /admin",
                             parse_mode="HTML")
    else:
        await message.answer(welcome_text, reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "📚 <b>Доступные команды:</b>\n\n"
        "/start - Запустить бота\n"
        "/help - Помощь\n"
        "/inline - Показать инлайн меню\n"
        "/keyboard - Показать основную клавиатуру"
    )

    # Добавляем админские команды если пользователь админ
    if await is_admin(message.from_user.id):
        help_text += "\n\n<b>👑 Команды администратора:</b>\n"
        help_text += "/admin - панель администратора\n"
        help_text += "/stats - статистика\n"
        help_text += "/broadcast - рассылка\n"
        help_text += "/users - список пользователей"

    await message.answer(help_text, parse_mode="HTML", reply_markup=get_main_keyboard())


@router.message(Command("inline"))
async def cmd_inline(message: types.Message):
    await message.answer("🔘 Выберите действие:", reply_markup=get_inline_keyboard())


@router.message(Command("keyboard"))
async def cmd_keyboard(message: types.Message):
    if await is_admin(message.from_user.id):
        await message.answer("⌨️ Панель администратора:", reply_markup=get_admin_keyboard())
    else:
        await message.answer("⌨️ Основное меню:", reply_markup=get_main_keyboard())


@router.message(Command("admin"))
async def cmd_admin_direct(message: types.Message):
    """Прямой обработчик команды /admin"""
    from handlers.admin import cmd_admin
    await cmd_admin(message)