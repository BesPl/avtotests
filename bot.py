import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config.data import Data
# Инициализация бота
TELEGRAM_TOKEN = f"{Data.TELEGRAM_TOKEN}"  # Замените на ваш токен
CHAT_ID = f"{Data.CHAT_ID}"  # Замените на ID вашей группы или чата

bot = Bot(token=TELEGRAM_TOKEN)

async def send_message_async(text):
    """Асинхронная функция для отправки сообщений."""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except TelegramError as e:
        print(f"Ошибка при отправке сообщения: {e}")

def send_message(text):
    """Синхронная обертка для асинхронной отправки сообщений."""
    asyncio.run(send_message_async(text))