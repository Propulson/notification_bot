import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

# Импортируем роутеры из отдельных файлов
from handlers.commands import router as commands_router
from handlers.callback import router as callback_router
from handlers.messages import router as messages_router
from handlers.admin import router as admin_router

# Инициализация базы данных
from database.base import init_db

# Проверка токена перед запуском
if not BOT_TOKEN or ":" not in BOT_TOKEN:
    print("❌ ОШИБКА: Неверный токен!")
    print("📝 Получите токен у @BotFather командой /newbot")
    exit(1)

# Инициализация базы данных
init_db()
print("✅ База данных инициализирована")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрируем все роутеры
dp.include_router(admin_router)
dp.include_router(commands_router)
dp.include_router(callback_router)
dp.include_router(messages_router)

print("✅ Все роутеры зарегистрированы")

async def main():
    print("🤖 Запуск бота...")
    print(f"✅ Токен: {BOT_TOKEN[:10]}...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())