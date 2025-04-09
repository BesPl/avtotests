#BasePage
import allure
import os
from logger_all import setup_logger
from allure_commons.types import AttachmentType
from datetime import datetime
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
        with allure.step(f"Страница  {self.PAGE_URL} открыта"):
            try:
                self.wait.until(EC.url_to_be(self.PAGE_URL))
                self.logger.info(f"Открыта {self.PAGE_URL} страница")
            except Exception as e:
                self.logger.error(f"Ошибка при открытии {self.PAGE_URL} страницы: {str(e)}")
                self.logger.error(f"Текущий URL: {self.driver.current_url}")

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
        # Создаем папку screenshots, если она не существует
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        # Генерируем уникальное имя файла с меткой времени
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{screenshot_name}_{timestamp}.png"
        file_path = os.path.join(screenshots_dir, file_name)

        # Сохраняем скриншот в файл
        self.driver.save_screenshot(file_path)

        # Прикрепляем скриншот к отчету Allure
        with open(file_path, "rb") as screenshot_file:
            allure.attach(
                body=screenshot_file.read(),
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

    def check_text_message(self, locator, expected_text):
        """
        Проверяет текст элемента.
        :param locator: Локатор элемента (например, (By.CLASS_NAME, "error-message-container"))
        :param expected_text: Ожидаемый текст для сравнения
        """
        try:
            # Находим элемент с текстом
            text_element = self.find_element(locator)  # Ищем элемент по локатору
            actual_text = text_element.text

            # Сравниваем фактический текст с ожидаемым
            assert actual_text == expected_text, \
                f"Ожидалось сообщение '{expected_text}', но получено '{actual_text}'"

            # Логируем успешную проверку
            self.logger.info(f"Текст корректный: '{actual_text}'")

        except AssertionError as e:
            # Логируем ошибку и фактический текст
            self.logger.error(f"Ошибка проверки текста: {e}")
            self.logger.error(f"Фактический текст: '{actual_text}'")
            raise  # Перебрасываем исключение для пометки теста как упавшего

    def check_src(self, locator, expected_text):
        """
        Проверяет текст элемента.
        :param locator: Локатор элемента (например, (By.CLASS_NAME, "error-message-container"))
        :param expected_text: Ожидаемая ссылка для сравнения
        """
        img_element = self.find_element(locator)
        img_src = img_element.get_attribute("src")
        product_name = img_element.get_attribute("alt")
        try:
            assert img_src == expected_text, \
                f"Ожидалось фото '{expected_text}', но получено '{img_src}'"
            # Логируем успешную проверку
            self.logger.info("Фото совпадает")
        except AssertionError as e:
            # Логируем ошибку и фактический текст
            self.make_screenshot(f"Неверное фото у {product_name}")
            self.logger.error(f"Ошибка проверки фото у {product_name}: {e}")
            self.logger.error(f"Фактическая ссылка на фото: '{img_src}'")
            raise  # Перебрасываем исключение для пометки теста как упавшего