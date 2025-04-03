import pytest
import allure
import os
from selenium import webdriver
from datetime import datetime


@pytest.fixture(scope="session", autouse=True)
def driver(request):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--incognito") #когда открывается в инкогнито
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

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