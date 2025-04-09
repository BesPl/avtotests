from Base.BasePage import BasePage
from config.links import Links
from selenium.webdriver.common.by import By
from config.data import Data
from selenium.webdriver.support import expected_conditions as EC
import allure

class InventoryPage(BasePage):
    PAGE_URL = Links.INVENTORY_PAGE

class Sauce_Labs_Backpack(BasePage):
    PAGE_URL = Links.INVENTORY_PAGE
    name_product = (By.CSS_SELECTOR, '*[data-test="inventory-item-name"]')
    foto_product = (By.CSS_SELECTOR, '*[data-test="inventory-item-sauce-labs-backpack-img"]')
    discription = (By.CSS_SELECTOR, '*[data-test="inventory-item-desc"]')
    price = (By.CSS_SELECTOR, '*[data-test="inventory-item-price"]')
    add_to_cart = (By.CSS_SELECTOR, '*[data-test="add-to-cart-sauce-labs-backpack"]')
    remove = (By.CSS_SELECTOR, '*[data-test="remove-sauce-labs-backpack"]')
    cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
    corect_disc1 = "Sauce Labs Backpack with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."
    corect_price1 = "$29.99"
    corect_name1 = "Sauce Labs Backpack"
    corect_src = "https://www.saucedemo.com/static/media/sauce-backpack-1200x1500.0a0b85a3.jpg"

    @allure.step("Нажатие на название товара: проверка кликабельности и перехода к странице товара")
    def click_name(self):
        self.logger.info("Нажатие на название объекта")
        self.click_element(self.name_product)

    @allure.step("Нажатие на изображение товара: проверка кликабельности и перехода к странице товара")
    def click_foto(self):
        self.logger.info("Нажатие на фото")
        self.click_element(self.foto_product)

    @allure.step("Проверка описания товара: сравнение с эталонным значением")
    def corect_discription(self):
        self.logger.info("Проверка что описание верное")
        self.check_text_message(self.discription, self.corect_disc1)

    @allure.step("Проверка цены товара: сравнение с ожидаемым значением")
    def corect_price(self):
        self.logger.info("Проверка что цена верная")
        self.check_text_message(self.price, self.corect_price1)

    @allure.step("Добавление товара в корзину через кнопку")
    def click_add_to_cart(self):
        self.logger.info("Нажатие на кнопку добавления в корзину")
        self.click_element(self.add_to_cart)

    @allure.step("Удаление товара из корзины через кнопку")
    def click_remove(self):
        self.logger.info("Нажатие на кнопку удаления из корзины")
        self.click_element(self.remove)
        self.make_screenshot("При удалении товара из корзины пропадает счетчик в корзине")

    @allure.step("Проверка увеличения счетчика корзины на 1")
    def corec_counter_plus(self):
        self.logger.info("Проверка увеличения на 1 счетчика в корзине при добавлении товара")
        badge = self.find_element(self.cart_badge)
        with allure.step(f"Проверка значения счетчика: ожидается '1', получено '{badge.text}'"):
            assert badge.text == "1", f"Ожидалось значение '1', но получено '{badge.text}'"
        self.logger.info("Значение счетчика увеличилось на 1.")

    @allure.step("Проверка названия товара: сравнение с эталонным значением")
    def corect_name(self):
        self.logger.info("Проверка что название верно")
        self.check_text_message(self.name_product, self.corect_name1)

    @allure.step("Проверка фото товара: сравнение с эталонным значением")
    def corect_foto(self):
        self.logger.info("Проверка фото продукта")
        self.check_src(self.foto_product, self.corect_src)






class Main_page_Sauce_Labs_Backpack(BasePage):
    PAGE_URL = Links.Sauce_Labs_Backpack_Page
    back_to_products2 = (By.CSS_SELECTOR, '*[data-test="back-to-products"]')
    name_product = (By.CSS_SELECTOR, '*[data-test="inventory-item-name"]')
    discription = (By.CSS_SELECTOR, '*[data-test="inventory-item-desc"]')
    price = (By.CSS_SELECTOR, '*[data-test="inventory-item-price"]')
    add_to_cart2 = (By.CSS_SELECTOR, '*[data-test="add-to-cart"]')
    remove2 = (By.CSS_SELECTOR, '*[data-test="remove"]')
    foto_product = (By.CSS_SELECTOR, '*[data-test="item-sauce-labs-backpack-img"]')
    cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

    corect_src = "https://www.saucedemo.com/static/media/sauce-backpack-1200x1500.0a0b85a3.jpg"
    corect_disc1 = "Sauce Labs Backpack with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."
    corect_price1 = "$29.99"
    corect_name1 = "Sauce Labs Backpack"

    @allure.step("Нажатие на кнопку back_to_products, для возврата из окна продукта")
    def click_back_to_products(self):
        self.logger.info("Нажатие на кнопку back_to_products, для возврата из окна продукта")
        self.click_element(self.back_to_products2)

    @allure.step("Проверка цены товара на странице товара: сравнение с ожидаемым значением")
    def corect_price(self):
        self.logger.info("Проверка что цена верная")
        self.check_text_message(self.price, self.corect_price1)

    @allure.step("Проверка названия товара на странице товара: сравнение с эталонным значением")
    def corect_name(self):
        self.logger.info("Проверка что название верно")
        self.check_text_message(self.name_product, self.corect_name1)

    @allure.step("Проверка описания товара на странице товара: сравнение с эталонным значением")
    def corect_discription(self):
        self.logger.info("Проверка что описание верное")
        self.check_text_message(self.discription, self.corect_disc1)

    @allure.step("Проверка увеличения счетчика корзины на 1, на странице товара")
    def corec_counter_plus(self):
        self.logger.info("Проверка увеличения на 1 счетчика в корзине при добавлении товара")
        badge = self.find_element(self.cart_badge)
        with allure.step(f"Проверка значения счетчика: ожидается '1', получено '{badge.text}'"):
            assert badge.text == "1", f"Ожидалось значение '1', но получено '{badge.text}'"
        self.logger.info("Значение счетчика увеличилось на 1.")

    @allure.step("Проверка фото товара на странице товара: сравнение с эталонным значением")
    def corect_foto(self):
        self.logger.info("Проверка фото продукта")
        self.check_src(self.foto_product, self.corect_src)

    @allure.step("Добавление товара в корзину через кнопку, на странице товара")
    def click_add_to_cart(self):
        self.logger.info("Нажатие на кнопку добавления в корзину")
        self.click_element(self.add_to_cart2)

    @allure.step("Удаление товара из корзины через кнопку, на странице товара")
    def click_remove(self):
        self.logger.info("Нажатие на кнопку удаления из корзины")
        self.click_element(self.remove2)
        self.make_screenshot("При удалении товара из корзины пропадает счетчик в корзине")