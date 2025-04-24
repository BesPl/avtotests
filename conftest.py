import allure
import os
import json
from selenium import webdriver
import pytest
from logger_all import setup_logger
from Base.BasePage import BasePage


# Фикстура для основного драйвера (создается всегда)
@pytest.fixture(scope="session")
def driver(request):
    """Фикстура для основного драйвера (создается всегда)."""
    logger = setup_logger(request.node.name)
    logger.info("Создание основного драйвера...")

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

    # Создаем драйвер в зависимости от выбранного браузера
    if browser_name == "firefox":
        driver_instance = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        driver_instance = webdriver.Edge(options=options)
    else:
        driver_instance = webdriver.Chrome(options=options)

    yield driver_instance
    logger.info("Закрытие основного драйвера...")
    driver_instance.quit()

@pytest.fixture(scope="function", autouse=True)
def setup_function(request, driver):
    """
    Фикстура для подготовки тестового окружения.
    Не создает изолированный драйвер автоматически.
    """
    request.cls.driver = driver
    yield
    driver.delete_all_cookies()

# Фикстура для изолированного драйвера (создается только для тестов с маркером)
@pytest.fixture(scope="function")
def isolated_driver(request):
    """Фикстура для создания изолированного драйвера."""
    logger = setup_logger(request.node.name)

    # Проверяем наличие маркера isolated_driver
    if not request.node.get_closest_marker("isolated_driver"):
        pytest.skip("Skipping isolated driver setup for non-isolated test")

    logger.info("Создание изолированного драйвера...")

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
    logger.info("Закрытие изолированного драйвера...")
    driver_instance.quit()

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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Создаёт скриншот при ошибке в логе или падении теста.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if hasattr(item, "function"):
            driver = item.funcargs.get("driver", None)
            if driver:
                screenshot_name = f"{item.name}_screenshot.png"
                screenshot_dir = "ERR_screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, screenshot_name)
                driver.save_screenshot(screenshot_path)
                driver.save_screenshot(screenshot_name)
                with open(screenshot_name, "rb") as file:
                    screenshot = file.read()
                allure.attach(screenshot, name=screenshot_name, attachment_type=allure.attachment_type.PNG)

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

# Хук для сохранения результатов теста в request.node
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Сохраняем результаты каждого этапа теста (setup, call, teardown)
    if report.when == "call":
        setattr(item, "rep_call", report)  # Сохраняем результат выполнения теста


