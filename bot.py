import asyncio
import threading
from telegram import Bot
from telegram.error import TelegramError
from config.data import Data


# Инициализация данных из конфига
TELEGRAM_TOKEN = Data.TELEGRAM_TOKEN
CHAT_ID = Data.CHAT_ID

# Создаем экземпляр бота вне функций
bot = Bot(token=TELEGRAM_TOKEN) if TELEGRAM_TOKEN and CHAT_ID else None

async def send_message_async(text):
    """Асинхронная функция для отправки сообщений."""
    if not bot:
        print("Бот не инициализирован: отсутствует токен или ID чата.")
        return

    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
        print("Сообщение успешно отправлено в Telegram.")
    except TelegramError as e:
        print(f"Ошибка при отправке сообщения через Telegram: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка при отправке: {e}")

def send_message(text):
    """Синхронная обертка для асинхронной отправки с использованием отдельного потока."""

    def run_async():
        asyncio.run(send_message_async(text))

    if not bot:
        print("Отправка сообщения отключена: бот не инициализирован.")
        return

    # Запуск в отдельном потоке, чтобы не блокировать pytest
    thread = threading.Thread(target=run_async)
    thread.start()