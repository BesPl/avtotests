import allure
from logger_all import setup_logger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            self.wait.until(EC.url_to_be(self.PAGE_URL))
            self.logger.info(f"Открыта {self.PAGE_URL} страница")
