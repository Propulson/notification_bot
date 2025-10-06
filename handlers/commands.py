from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import get_main_keyboard, get_admin_keyboard
from keyboards.inline import get_inline_keyboard
from utils.users import get_or_create_user, is_admin

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
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

    if await is_admin(message.from_user.id):
        await message.answer(welcome_text, reply_markup=get_admin_keyboard())
        await message.answer("👑 <b>Вам доступна панель администратора!</b>\nИспользуйте /admin",
                             parse_mode="HTML")
    else:
        await message.answer(welcome_text, reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = ("Test")

    if await is_admin(message.from_user.id):
        help_text += "\n\n<b>👑 Команды администратора:</b>\n"
        help_text += "/admin - панель администратора\n"
        help_text += "/stats - статистика\n"
        help_text += "/broadcast - рассылка\n"
        help_text += "/users - список пользователей"

    await message.answer(help_text, parse_mode="HTML", reply_markup=get_main_keyboard())


@router.message(Command("inline"))
async def cmd_inline(message: types.Message):
    from keyboards.inline import get_inline_keyboard
    await message.answer("🔘 Выберите действие:", reply_markup=get_inline_keyboard())


@router.message(Command("keyboard"))
async def cmd_keyboard(message: types.Message):
    if await is_admin(message.from_user.id):
        from keyboards.reply import get_admin_keyboard
        await message.answer("⌨️ Панель администратора:", reply_markup=get_admin_keyboard())
    else:
        from keyboards.reply import get_main_keyboard
        await message.answer("⌨️ Основное меню:", reply_markup=get_main_keyboard())