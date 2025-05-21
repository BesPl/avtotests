import asyncio
import threading
from telegram import Bot
import requests
from telegram.error import TelegramError
from config.data import Data


# Инициализация данных из конфига
TELEGRAM_TOKEN = Data.TELEGRAM_TOKEN
CHAT_ID = Data.CHAT_ID

# Создаем экземпляр бота вне функций
bot = Bot(token=TELEGRAM_TOKEN) if TELEGRAM_TOKEN and CHAT_ID else None
def send_message(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("🚫 Токен или chat_id не заданы")
        return

    url = f"https://api.telegram.org/bot {TELEGRAM_TOKEN}/sendMessage"

    def send():
        try:
            response = requests.post(
                url,
                data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
            )
            if response.status_code == 200:
                print("✅ Сообщение успешно отправлено в Telegram")
            else:
                print(f"❌ Ошибка отправки: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"⚠️ Не удалось отправить сообщение: {e}")

    thread = threading.Thread(target=send)
    thread.start()