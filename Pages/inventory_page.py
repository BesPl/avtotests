from Base.BasePage import BasePage
from config.links import Links
from selenium.webdriver.common.by import By
from config.data import Data
from selenium.webdriver.support import expected_conditions as EC
import allure


class InventoryPage (BasePage):
    PAGE_URL = Links.INVENTORY_PAGE


class Sauce_Labs_Backpack(BasePage):
    PAGE_URL = Links.Sauce_Labs_Backpack_Page
    name_product = (By.CSS_SELECTOR, '*[data-test="inventory-item-name"]')
    foto_product = (By.CSS_SELECTOR, '*[data-test="inventory-item-sauce-labs-backpack-img"]')
    discription = (By.CSS_SELECTOR, '*[data-test="inventory-item-desc"]')
    price = (By.CSS_SELECTOR, '*[data-test="inventory-item-price"]')
    add_to_cart = (By.CSS_SELECTOR, '*[data-test="add-to-cart-sauce-labs-backpack"]')
    remove = (By.CSS_SELECTOR, '*[data-test="remove-sauce-labs-backpack"]')
    expected_error = "Sauce Labs Backpack with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."

    def click_name(self):
        self.click_element(self.name_product)
        self.logger.info("Нажатие на название объекта")

    def click_foto(self):
        self.click_element(self.foto_product)
        self.logger.info("")

    def corect_discription(self):
        self.check_text_message(self.discription, self.expected_error)

