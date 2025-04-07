import pytest
import allure
from Base.BaseTest import BaseTest


@allure.feature("Profile Functionality")
class TestProfileFeature(BaseTest):

    @allure.title("Успешная авторизация с корректными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_correct_login(self):
        self.login_page.open()
        self.login_page.is_opened()
        self.login_page.corect_login()

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