import time

from Base.BasePage import BasePage
from config.links import Links
from selenium.webdriver.common.by import By
from config.data import Data
from selenium.webdriver.support import expected_conditions as EC
import allure


class LoginPage(BasePage):
    PAGE_URL = Links.MAIN_PAGE
    pole_login = (By.CSS_SELECTOR, '*[data-test="username"]')
    pole_pass = (By.CSS_SELECTOR, '*[data-test="password"]')
    login_button = (By.CSS_SELECTOR, '*[data-test="login-button"]')
    error_text = (By.CSS_SELECTOR, '*[data-test="error"]')
    error_button = (By.CLASS_NAME, 'error-button')

    @allure.step("Ввод корректного логина")
    def input_corect_login(self):
        self.logger.info("Ввод корректного логина")
        self.input_credentials(self.pole_login, Data.LOGIN)

    @allure.step("Ввод корректного пароля")
    def input_corect_pass(self):
        self.logger.info("Ввод корректного пароля")
        self.input_credentials(self.pole_pass, Data.PASSWORD)

    @allure.step("Клик по кнопке логин")
    def click_login_button(self):
        self.logger.info("Клик по кнопке логин")
        self.click_element(self.login_button)

    @allure.step("Ввод некорректного логина")
    def input_uncorect_login(self):
        self.logger.info("Ввод некорректного логина")
        self.input_credentials(self.pole_login, "uncorect_login")

    @allure.step("Ввод некорректного пароля")
    def input_uncorect_pass(self):
        self.logger.info("Ввод некорректного пароля")
        self.input_credentials(self.pole_pass, "uncorect_pass")

    @allure.step("Проверка текста ошибки при некорректных данных")
    def check_error_incorrect(self):
        try:
            actual_error = self.find_element(self.error_text).text
            assert actual_error == "Epic sadface: Username and password do not match any user in this service", \
                f"Ожидалось сообщение 'Epic sadface: Username and password do not match any user in this service', но получено '{actual_error}'"
            self.logger.info("Текст ошибки корректный")
        except AssertionError as e:
            # Логируем фактический текст ошибки
            self.logger.error(f"Ошибка проверки текста: {e}")
            self.logger.error(f"Фактический текст ошибки: {self.find_element(self.error_text).text}")
            raise  # Повторно выбрасываем исключение, чтобы тест был помечен как неудачный

    @allure.step("Клик по кнопке закрытия ошибки")
    def click_error_button(self):
        self.logger.info("Клик по кнопке закрытия ошибки")
        self.click_element(self.error_button)

    @allure.step("Ввод заблокированного пользователя")
    def input_locked_out_user(self):
        self.logger.info("Ввод заблокированного пользователя")
        self.input_credentials(self.pole_login, Data.locked_out)

    @allure.step("Проверка текста ошибки при заблокированном пользователе")
    def check_error_locked_out(self):
        try:
            actual_error = self.find_element(self.error_text).text
            assert actual_error == "Epic sadface: Sorry, this user has been locked out.", \
                f"Ожидалось сообщение 'Epic sadface: Sorry, this user has been locked out.', но получено '{actual_error}'"
            self.logger.info("Текст ошибки корректный")
        except AssertionError as e:
            # Логируем фактический текст ошибки
            self.logger.error(f"Ошибка проверки текста: {e}")
            self.logger.error(f"Фактический текст ошибки: {self.find_element(self.error_text).text}")
            raise  # Повторно выбрасываем исключение, чтобы тест был помечен как неудачный

    @allure.step("Проверка ошибки при нажатии кнопки входа без логина и пароля")
    def username_required(self):
        try:
            actual_error = self.find_element(self.error_text).text
            assert actual_error == "Epic sadface: Username is required", \
                f"Ожидалось сообщение 'Epic sadface: Username is required', но получено '{actual_error}'"
            self.logger.info("Текст ошибки корректный")
        except AssertionError as e:
            # Логируем фактический текст ошибки
            self.logger.error(f"Ошибка проверки текста: {e}")
            self.logger.error(f"Фактический текст ошибки: {self.find_element(self.error_text).text}")
            raise  # Повторно выбрасываем исключение, чтобы тест был помечен как неудачный

    @allure.step(f"Проверка ошибки при переходе на страницу {Links.INVENTORY_PAGE} без авторизации")
    def access_wthen_not_liggin(self):
        try:
            actual_error = self.find_element(self.error_text).text
            assert actual_error == "Epic sadface: You can only access '/inventory.html' when you are logged in.", \
                f"Ожидалось сообщение 'Epic sadface: You can only access '/inventory.html' when you are logged in.', но получено '{actual_error}'"
            self.logger.info("Текст ошибки корректный")
        except AssertionError as e:
            # Логируем фактический текст ошибки
            self.logger.error(f"Ошибка проверки текста: {e}")
            self.logger.error(f"Фактический текст ошибки: {self.find_element(self.error_text).text}")
            raise  # Повторно выбрасываем исключение, чтобы тест был помечен как неудачный

    @allure.step("Выполнение корректной авторизации")
    def corect_login(self):
        self.input_corect_login()
        self.input_corect_pass()
        self.click_login_button()

    @allure.step("Проверка авторизации с некорректными данными")
    def incorrect_login(self):
        self.input_uncorect_login()
        self.input_uncorect_pass()
        self.click_login_button()
        self.check_error_incorrect()
        self.click_error_button()

    @allure.step("Проверка авторизации заблокированного пользователя")
    def locked_out_user(self):
        self.input_locked_out_user()
        self.input_corect_pass()
        self.click_login_button()
        self.check_error_locked_out()
        self.click_error_button()

    @allure.step("Проверка входа без ввода логи и пароля")
    def try_com_page_without_login(self):
        self.click_login_button()
        self.username_required()

