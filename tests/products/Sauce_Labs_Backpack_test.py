import time

import pytest
import allure
from Base.BaseTest import BaseTest
from config.links import Links

@allure.feature("Inventory Functionality")
class Test_Sauce_Labs_Backpack(BaseTest):

    @allure.title("Проверка описания товара")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_correct_discription(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.sauce_labs_backpack.corect_discription()

    @allure.title("Проверка цены товара")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_correct_price(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.sauce_labs_backpack.corect_price()

    @allure.title("Проверка названия товара")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_correct_name(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.sauce_labs_backpack.corect_name()

    @allure.title("Проверка добавления товара в корзину")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_add_Backpack_в_корзину(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.sauce_labs_backpack.click_add_to_cart()
        self.sauce_labs_backpack.corec_counter_plus()
        self.sauce_labs_backpack.click_remove()

    @allure.title("Проверка нажатие_на_название_рюкзака_с_переходом_на_страницу_продукта")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_нажатие_на_название_рюкзака_с_переходом_на_страницу_продукта(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.sauce_labs_backpack.click_name()
        self.main_page_sauce_Labs_Backpack.is_opened()
        self.main_page_sauce_Labs_Backpack.click_back_to_products()
        self.inventory_page.is_opened()

    @allure.title("Проверка нажатие_на_фото_рюкзака_с_переходом_на_страницу_продукта")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_нажатие_на_фото_рюкзака_с_переходом_на_страницу_продукта(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.sauce_labs_backpack.click_foto()
        self.main_page_sauce_Labs_Backpack.is_opened()
        self.main_page_sauce_Labs_Backpack.click_back_to_products()
        self.inventory_page.is_opened()

    @allure.title("Проверка фото товара")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_correct_foto(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.sauce_labs_backpack.corect_foto()

    @allure.title("Проверка фото товара, на странице Backpack")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_correct_foto_Backpack_page(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.main_page_sauce_Labs_Backpack.open()
        self.main_page_sauce_Labs_Backpack.is_opened()
        self.main_page_sauce_Labs_Backpack.corect_foto()

    @allure.title("Проверка добавления товара в корзину, на странице Backpack")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_add_Backpack_в_корзину_Backpack_page(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.main_page_sauce_Labs_Backpack.open()
        self.main_page_sauce_Labs_Backpack.click_add_to_cart()
        self.main_page_sauce_Labs_Backpack.corec_counter_plus()
        self.main_page_sauce_Labs_Backpack.click_remove()

    @allure.title("Проверка описания товара, на странице Backpack")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_correct_discription_Backpack_page(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.main_page_sauce_Labs_Backpack.open()
        self.main_page_sauce_Labs_Backpack.corect_discription()

    @allure.title("Проверка цены товара, на странице Backpack")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_correct_price_Backpack_page(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.main_page_sauce_Labs_Backpack.open()
        self.main_page_sauce_Labs_Backpack.corect_price()

    @allure.title("Проверка названия товара, на странице Backpack")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_correct_name_Backpack_page(self):
        self.login_page.open()
        self.login_page.corect_login()
        self.main_page_sauce_Labs_Backpack.open()
        self.main_page_sauce_Labs_Backpack.corect_name()