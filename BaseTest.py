import pytest
from login_page import LoginPage
from logger_all import setup_logger

class BaseTest:
    login_page = LoginPage

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)  # Создаем экземпляр LoginPage
        self.logger = setup_logger(self.__class__.__name__)  # Логгер для тестового класса

