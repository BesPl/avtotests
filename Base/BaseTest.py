import pytest
from Pages.login_page import LoginPage
from Pages.inventory_page import InventoryPage
from logger_all import setup_logger
from config.data import Data



class BaseTest:
    login_page = LoginPage
    inventory_page = InventoryPage
    data = Data


    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.data = Data
        self.inventory_page = InventoryPage(driver)
        self.login_page = LoginPage(driver)  # Создаем экземпляр LoginPage
        self.logger = setup_logger(self.__class__.__name__)  # Логгер для тестового класса

