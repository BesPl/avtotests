#BasePage
import allure
from logger_all import setup_logger
from allure_commons.types import AttachmentType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10, poll_frequency=1)
        self.logger = setup_logger(self.__class__.__name__)

    def open(self):
        with allure.step(f"Открытие {self.PAGE_URL} страницы"):
            self.driver.get(self.PAGE_URL)
            self.logger.info(f"Открытие {self.PAGE_URL} страницы")

    def is_opened(self):#ожидание открытия страницы
        with allure.step(f"Page {self.PAGE_URL} is opened"):
            try:
                self.wait.until(EC.url_to_be(self.PAGE_URL))
                self.logger.info(f"Открыта {self.PAGE_URL} страница")
            except Exception as e:
                self.logger.error(f"Ошибка при открытии {self.PAGE_URL} страницы: {str(e)}")

    def find_element(self, locator, timeout=10):
        """Ожидает появление элемента и возвращает его"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator),
                message=f"Элемент {locator} не найден за {timeout} секунд"
            )
        except Exception as e:
            self.logger.error(f"Ошибка поиска элемента {locator}: {e}")

    def enter_text(self, locator, text):
        """Очищает поле и вводит текст"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Введено: '{text}' в элемент {locator}")

    def click_element(self, locator):
        """Кликает на элемент после проверки его кликабельности"""
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не кликабелен"
        )
        element.click()
        self.logger.debug(f"Клик выполнен: {locator}")

    def make_screenshot(self, screenshot_name):
        allure.attach(
            body=self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=AttachmentType.PNG
        )

    def refresh(self):
        """Обновляет страницу и проверяет её загрузку"""
        self.logger.info("Выполняю обновление страницы")
        self.driver.refresh()

        # Явное ожидание перезагрузки страницы
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.logger.info("Страница успешно обновлена")

    def input_credentials(self, field_locator, value):
        self.click_element(field_locator)
        self.enter_text(field_locator, value)