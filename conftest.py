import allure
import os
import json
from selenium import webdriver
import pytest
from logger_all import setup_logger
from Base.BasePage import BasePage
from datetime import datetime
from bot import send_message

@pytest.fixture(scope="session", autouse=True)
def driver(request):
    config = load_config()
    browser_name = config["BROWSER"].lower()
    headless = config["HEADLESS"]
    if request.node.get_closest_marker("needs_isolation"):
        pytest.skip("Skipping shared driver for isolated test")
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--incognito")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    if headless:
        options.add_argument("--headless=new")

    # Создаем драйвер в зависимости от выбранного браузера
    if browser_name == "firefox":
        driver_instance = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        driver_instance = webdriver.Edge(options=options)
    else:
        driver_instance = webdriver.Chrome(options=options)

    # Используем один экземпляр драйвера
    yield driver_instance
    driver_instance.quit()

@pytest.fixture(scope="function", autouse=True)
def setup_function(request, driver):
    """Фикстура для подготовки тестового окружения."""
    request.cls.driver = driver
    yield
    driver.delete_all_cookies()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для сохранения результатов теста в request.node.
    Добавляет создание скриншотов при ошибках в тестах.
    """
    outcome = yield
    report = outcome.get_result()

    # Сохраняем результат выполнения теста
    if report.when == "call":
        setattr(item, "rep_call", report)  # Сохраняем результат выполнения теста

        # Проверяем, что тест завершился с ошибкой и есть драйвер
        if report.failed and hasattr(item, "funcargs"):
            driver = item.funcargs.get("driver") or item.funcargs.get("isolated_driver")
            if driver and isinstance(driver, webdriver.Remote):  # Убедимся, что это Selenium WebDriver
                # Создаем папку для скриншотов, если она не существует
                screenshot_folder = "ERR_screenshots"
                os.makedirs(screenshot_folder, exist_ok=True)

                # Формируем имя файла скриншота
                test_name = item.name
                screenshot_file = os.path.join(screenshot_folder, f"{test_name}.png")

                # Делаем скриншот
                try:
                    driver.save_screenshot(screenshot_file)
                    print(f"Скриншот сохранен: {screenshot_file}")
                except Exception as e:
                    print(f"Ошибка при создании скриншота: {e}")

def load_config():
    """Загрузка конфигурации из файла config.json с проверкой обязательных полей"""
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            required_fields = ["BROWSER", "HEADLESS"]
            for field in required_fields:
                if field not in config:
                    config[field] = {"BROWSER": "chrome", "HEADLESS": True}[field]
            return config
    except (FileNotFoundError, json.JSONDecodeError):
        return {"BROWSER": "chrome", "HEADLESS": True}

@pytest.fixture(autouse=True)
def auto_logging(request):
    # Инициализация логгера
    logger = setup_logger(request.node.name)

    # Получаем название из Allure
    allure_title = request.node.get_closest_marker('allure_title')
    test_name = allure_title.args[0] if allure_title else request.node.name

    # Логирование начала теста
    logger.info(f"====== Запуск теста: {test_name} ======")

    yield  # Выполнение теста

    # Определение статуса теста
    report = getattr(request.node, "rep_call", None)  # Доступ к результатам выполнения теста

    if report:
        if report.passed:
            logger.info(f"====== Тест успешно завершен: {test_name} ======")
        elif report.failed:
            logger.error(f"====== Тест упал: {test_name} | Причина: {report.longrepr} ======")
        elif report.skipped:
            logger.warning(f"====== Тест пропущен: {test_name} ======")

    logger.info("=" * 60)

@pytest.fixture(scope="function")
def isolated_driver(request):
    """Фикстура для создания дополнительной сессии драйвера."""
    config = load_config()
    browser_name = config["BROWSER"].lower()
    headless = config["HEADLESS"]

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--incognito")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    if headless:
        options.add_argument("--headless=new")

    # Создаем новый экземпляр драйвера
    if browser_name == "firefox":
        driver_instance = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        driver_instance = webdriver.Edge(options=options)
    else:
        driver_instance = webdriver.Chrome(options=options)

    yield driver_instance
    # Закрываем дополнительную сессию после теста
    driver_instance.quit()

@pytest.fixture(scope="session", autouse=True)
def send_summary(request):
    """
    Фикстура для отправки сводного отчета после завершения всех тестов.
    """
    session = request.session

    # Сохраняем время начала тестовой сессии
    start_time = datetime.now()

    summary = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "failed_tests": [],
        "skipped_tests": []
    }

    def _send_summary():
        # Собираем статистику по тестам
        summary["total"] = len(session.items)
        for item in session.items:
            if hasattr(item, "rep_call"):
                report = item.rep_call
                if report.passed:
                    summary["passed"] += 1
                elif report.failed:
                    summary["failed"] += 1
                    summary["failed_tests"].append(f"{item.name} (ошибка: {report.longrepr})")
                elif report.skipped:
                    summary["skipped"] += 1
                    reason = getattr(report, "wasxfail", "unknown")
                    summary["skipped_tests"].append(f"{item.name} (причина: {reason})")

        end_time = datetime.now()
        duration = end_time - start_time

        # Формируем сообщение
        message = (
            "📊 Тестирование завершено:\n"
            f"📜 Всего тестов: {summary['total']}\n"
            f"✅ Успешно: {summary['passed']}\n"
            f"❌ Провалено: {summary['failed']}\n"
            f"⚠️ Пропущено: {summary['skipped']}\n\n"
            f"⏱ Время выполнения: {duration.seconds // 60} мин {duration.seconds % 60} сек\n"
            f"📅 Дата начала: {start_time.date()}\n"
            f"⏰ Время начала: {start_time.strftime('%H:%M:%S')}\n\n"
        )

        # Добавляем информацию о проваленных тестах
        if summary["failed"] > 0:
            message += "📝 Проваленные тесты:\n"
            for test in summary["failed_tests"]:
                message += f"  - {test}\n"

        # Добавляем информацию о пропущенных тестах
        if summary["skipped"] > 0:
            message += "\n📝 Пропущенные тесты:\n"
            for test in summary["skipped_tests"]:
                message += f"  - {test}\n"

        # Отправляем сообщение в Telegram
        try:
            send_message(message)
            print("Сводный отчет отправлен через send_message.")
        except Exception as e:
            print(f"Ошибка при отправке сводного отчета: {e}")

    # Добавляем финализатор с небольшой задержкой
    def on_exit():
        import time
        time.sleep(2)  # Даем системе немного времени на закрытие драйвера
        _send_summary()

    request.addfinalizer(on_exit)