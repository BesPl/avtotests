import pytest
from Pages.login_page import LoginPage
from Pages.inventory_page import InventoryPage
from Pages.inventory_page import Sauce_Labs_Backpack
from Pages.inventory_page import Main_page_Sauce_Labs_Backpack
from logger_all import setup_logger
from config.data import Data



class BaseTest:
    login_page = LoginPage
    inventory_page = InventoryPage
    sauce_labs_backpack = Sauce_Labs_Backpack
    main_page_sauce_Labs_Backpack = Main_page_Sauce_Labs_Backpack
    data = Data


    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.data = Data
        self.main_page_sauce_Labs_Backpack = Main_page_Sauce_Labs_Backpack(driver)
        self.sauce_labs_backpack = Sauce_Labs_Backpack(driver)
        self.inventory_page = InventoryPage(driver)
        self.login_page = LoginPage(driver)  # Создаем экземпляр LoginPage
        self.logger = setup_logger(self.__class__.__name__)  # Логгер для тестового класса

