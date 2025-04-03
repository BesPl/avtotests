import pytest
import allure
import os
from selenium import webdriver


@pytest.fixture(scope="session", autouse=True)
def driver(request):
    """Фикстура для инициализации WebDriver (сессионная область видимости)."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Полноэкранный режим
    # options.add_argument("--headless=new")  # Запуск в фоне (без отображения окна)
    # options.add_argument("--disable-gpu")  # Отключение GPU (для headless)
    driver_instance = webdriver.Chrome(options=options)
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
        driver = item.cls.driver if hasattr(item, "cls") else None
        if driver:
            # Создаем папку для скриншотов, если она не существует
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            # Формируем имя файла и путь
            screenshot_name = f"screenshot_{item.name}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)
            # Сохраняем скриншот
            driver.save_screenshot(screenshot_path)
            # Прикрепляем скриншот к Allure-отчету
            allure.attach(
                body=driver.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )