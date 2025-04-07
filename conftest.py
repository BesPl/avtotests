import pytest
import allure
import os
import json
from selenium import webdriver
from datetime import datetime



@pytest.fixture(scope="session", autouse=True)
def driver(request):
    config = load_config()
    browser_name = config["BROWSER"].lower()
    headless = config["HEADLESS"]

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
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

# Автоматическое создание скриншота при падении теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = getattr(item, "driver", None) or getattr(item.cls, "driver", None)
        if driver:
            # Создаем скриншот с уникальным именем
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"failure_{item.name}_{timestamp}"

            # Сохраняем скриншот в файл
            screenshots_dir = os.path.join("screenshots", datetime.now().strftime("%Y-%m-%d"))
            os.makedirs(screenshots_dir, exist_ok=True)
            driver.save_screenshot(os.path.join(screenshots_dir, f"{screenshot_name}.png"))

            # Прикрепляем к Allure
            allure.attach(
                body=driver.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )

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