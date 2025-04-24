import time
import pytest
import allure
from Base.BaseTest import BaseTest


# @allure.feature("Create_user")
# class Test_create_user(BaseTest):
#     @allure.title("Проверка создания аккаунта с корректными данными c 2fa на DEV")
#     @allure.severity(allure.severity_level.CRITICAL)  # Критический тест
#     @pytest.mark.smoke  # Тест для проверки основной функциональности
#     @pytest.mark.create_user  # Метка для группировки тестов создания пользователей
#     @pytest.mark.dev  # Тест для DEV-окружения
#     @pytest.mark.positive
#     def test_CORRECT_create_user_DEV_2FA(self):
#         self.Dev_Login.open()
#         self.login_steos.corect_create_test_user_w2fa()
#         self.login_steos.check_err_login_without_invitation()
#         self.login_steos.delete_from_all_base()
#
#     @allure.title("Проверка создания аккаунта с некорректными данными на voice")
#     @allure.severity(allure.severity_level.MINOR)  # Низкоприоритетный тест
#     @pytest.mark.regression  # Регрессионный тест
#     @pytest.mark.create_user  # Метка для группировки тестов создания пользователей
#     @pytest.mark.voice  # Тест для Voice-окружения
#     @pytest.mark.negative
#     def test_ERR_INcorrect_create_user_VOICE(self):
#         self.voice.open()
#         self.login_steos.ERR_create()
#         self.voice.refresh()
#
#     @allure.title("Проверка создания аккаунта с корректными данными без 2fa на voice")
#     @allure.severity(allure.severity_level.CRITICAL)  # Критический тест
#     @pytest.mark.smoke  # Тест для проверки основной функциональности
#     @pytest.mark.create_user  # Метка для группировки тестов создания пользователей
#     @pytest.mark.voice  # Тест для Voice-окружения
#     @pytest.mark.positive
#     def test_CORRECT_create_user_VOICE(self):
#         self.voice.open()
#         self.login_steos.corect_create_test_user()
#         self.VOICE_main.is_opened()
#
#
# @allure.feature("Login_user")
# class Test_login_user(BaseTest):
#     @allure.title("Проверка входа на DEV без приглашения после  авторизации в ранее в браузере")
#     @allure.severity(allure.severity_level.CRITICAL)  # Критический тест
#     @pytest.mark.smoke  # Тест для проверки основной функциональности
#     @pytest.mark.login  # Метка для группировки тестов входа
#     @pytest.mark.positive
#     @pytest.mark.dev  # Тест для DEV-окружения
#     def test_сheck_login_user_VOICE_on_DEV_without_invitation(self):
#         self.Dev_Login.open()
#         self.login_steos.login_test_after_login()
#         self.login_steos.check_err_login_without_invitation()
#         self.DEV_main_page.is_not_opened()
#
#     @allure.title("Проверка входа на DEV с приглашением после авторизации в ранее в браузере")  # Сейчас без 2FA
#     @allure.severity(allure.severity_level.CRITICAL)  # Критический тест
#     @pytest.mark.smoke  # Тест для проверки основной функциональности
#     @pytest.mark.login  # Метка для группировки тестов входа
#     @pytest.mark.positive
#     @pytest.mark.dev  # Тест для DEV-окружения
#     def test_сheck_login_user_VOICE_on_DEV_with_invitation(self):
#         self.login_steos.create_invite()
#         self.Dev_Login.open()
#         self.login_steos.login_test_after_login()
#         self.DEV_main_page.is_opened()
#
#
#     @allure.title("Проверка входа на DEV без авторизации ранее с 2fa")  # Сейчас админ
#     @allure.severity(allure.severity_level.CRITICAL)  # Критический тест
#     @pytest.mark.smoke  # Тест для проверки основной функциональности
#     @pytest.mark.login  # Метка для группировки тестов входа
#     @pytest.mark.positive
#     @pytest.mark.dev  # Тест для DEV-окружения
#     @pytest.mark.isolated_driver
#     def test_сheck_login_user_on_DEV(self, isolated_setup):
#         self.isolated_login_steos.delete_from_2fa_STEOS()
#         self.isolated_Dev_Login.open()
#         self.isolated_login_steos.login2fa_admin_first_try_dev()
#         self.isolated_DEV_main_page.is_opened()

@allure.feature("SQL запросы")
class Test_sql(BaseTest):

    @allure.step("Удаление аккаунта из всех баз данных")
    @allure.severity(allure.severity_level.NORMAL)  # Средний уровень важности
    @pytest.mark.cleanup  # Метка для тестов очистки данных
    @pytest.mark.all_bases  # Метка для операций с несколькими базами данных
    def test_delete_user_from_all_base(self):
        self.login_steos.delete_from_all_base()