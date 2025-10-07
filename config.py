import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN ='BOT_TOKEN'

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Проверьте файл .env")