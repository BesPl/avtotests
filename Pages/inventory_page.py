from Base.BasePage import BasePage
from config.links import Links
from selenium.webdriver.common.by import By
from config.data import Data
from selenium.webdriver.support import expected_conditions as EC
import allure


class InventoryPage (BasePage):
    PAGE_URL = Links.INVENTORY_PAGE


