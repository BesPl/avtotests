import time

import pytest
import allure
from Base.BaseTest import BaseTest
from config.links import Links


@allure.feature("Login Functionality")
class TestLogin(BaseTest):

    @allure.title("Успешная авторизация с корректными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_correct_login(self):
        self.login_page.open()
        self.login_page.is_opened()
        self.login_page.corect_login()
        self.inventory_page.is_opened()

    @allure.title("Проверка авторизации с некорректными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_incorrect_login(self):
        self.login_page.open()
        self.login_page.is_opened()
        self.login_page.incorrect_login()

    @allure.title("Проверка авторизации заблокированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_locked_out_user(self):
        self.login_page.open()
        self.login_page.is_opened()
        self.login_page.locked_out_user()

    @allure.title("Проверка входа без ввода логи и пароля")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_comin_without_LogPas(self):
        self.login_page.open()
        self.login_page.is_opened()
        self.login_page.try_com_page_without_login()

    @allure.title(f"Проверка перехода на страницу {Links.INVENTORY_PAGE} без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_try_com_page_without_login(self):
        self.inventory_page.open()
        self.login_page.access_wthen_not_liggin()

# @allure.feature("Inventory Functionality")
# class TestInventory(BaseTest):
#
#     @allure.title("Успешная авторизация с корректными данными")
#     @allure.severity(allure.severity_level.CRITICAL)
#     @pytest.mark.smoke
#     def test_correct_discription(self):
#         self.login_page.open()
#         self.login_page.corect_login()
#         self.sauce_labs_backpack.corect_discription()