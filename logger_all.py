import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"  # Папка для логов
MAX_FILES = 5      # Максимальное количество файлов в день
MAX_SIZE_MB = 10   # Максимальный общий размер файлов в день (в МБ)

# Глобальная переменная для хранения времени начала записи лога
CURRENT_LOG_TIME = None

def setup_logger(name):
    """
    Настройка логгера для записи в файл и вывода ошибок в терминал.
    """
    global CURRENT_LOG_TIME

    # Создание директории, если она не существует
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Создание папки для логов по датам
    today_dir = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(LOG_DIR, today_dir)
    os.makedirs(log_path, exist_ok=True)
    manage_log_files(log_path)

    # Формат логов
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Создание логгера
    logger = logging.getLogger(name)  # Используем переданное имя
    logger.setLevel(logging.DEBUG)

    # Если у логгера уже есть обработчики, проверяем, нужно ли создавать новый файл
    if not logger.handlers:
        # Обработчик для терминала (только ошибки)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        console_handler.setLevel(logging.ERROR)
        logger.addHandler(console_handler)

        # Определяем имя файла лога
        current_time = datetime.now()
        if CURRENT_LOG_TIME is None or current_time.minute != CURRENT_LOG_TIME.minute:
            CURRENT_LOG_TIME = current_time
        file_name = f"{CURRENT_LOG_TIME.strftime('%H-%M')}.log"

        # Обработчик для файла
        file_handler = logging.FileHandler(os.path.join(log_path, file_name), encoding="utf-8")
        file_handler.setFormatter(log_format)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    return logger

def manage_log_files(log_path):
    """
    Удаляет старые файлы логов, если их количество превышает MAX_FILES
    или общий размер превышает MAX_SIZE_MB.
    """
    files = [os.path.join(log_path, f) for f in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, f))]
    files.sort(key=os.path.getmtime)  # Сортируем файлы по времени модификации

    # Удаляем старые файлы, если их количество превышает MAX_FILES
    while len(files) > MAX_FILES:
        os.remove(files[0])  # Удаляем самый старый файл
        files = files[1:]  # Обновляем список файлов

    # Удаляем старые файлы, если общий размер превышает MAX_SIZE_MB
    total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)  # Размер в МБ
    while total_size > MAX_SIZE_MB and files:
        os.remove(files.pop(0))
        total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)

def test_logger(logger):
    logger.debug("Это сообщение отладки")
    logger.info("Это информационное сообщение")
    logger.warning("Это предупреждение")
    logger.error("Это сообщение об ошибке")
    logger.critical("Это критическое сообщение")