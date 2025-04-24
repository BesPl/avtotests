import time
import pytest
from Base.BasePage import BasePage
from selenium.webdriver.common.by import By
from config.data import Data
from selenium.webdriver.support import expected_conditions as EC
import allure


class LoginSteos(BasePage):
    log_in_via = (By.CLASS_NAME, "button__content__container")
    mail_input = (By.CLASS_NAME, "have__left-icon")
    button_log_in = (By.CLASS_NAME, "content__container")
    pas_input = (By.ID, 'confirmLoginPassword')
    button_continue_as = (By.CLASS_NAME, "content__container")
    cod_mail = (By.XPATH, "//input [@placeholder ='Введите код подтверждения']")
    info_name = (By.CLASS_NAME, "login-info__name")
    info_email = (By.CLASS_NAME, "login-info__email")
    corect_name = "VoiceLastname VoicenameNAME"
    back_to_autorization = (By.CLASS_NAME, "controls__back-link")
    сonfirm = (By.CLASS_NAME,"content__container")
    button_continue_as_afte_login = (By.XPATH , '//*[@id="app"]/div/div[2]/div[2]/div/div[1]/div[2]/button[1]')
    error_login_dev = (By.XPATH, "//span[contains(text(), 'Вход невозможен без приглашения')]")
#=================
    email_address = f'{Data.ADMIN_LOGIN}'
    password = f'{Data.ADMIN_Mail_PASS}'
#=================

    @allure.step("Нажатие кнопки входа через SteosID")
    def click_login_via_Steos(self):
        self.logger.info("Выполняется нажатие на кнопку 'Вход через SteosID'")
        self.click_element(self.log_in_via)
        self.driver.implicitly_wait(10)

    @allure.step("Ввод почтового адреса администратора")
    def enter_mail_input_admin(self):
        self.driver.switch_to.frame("authIframe")
        self.logger.info("Ввод почтового адреса администратора")
        self.enter_text(self.mail_input, Data.ADMIN_LOGIN)

    @allure.step("Ввод почтового адреса тестового аккаунта")
    def enter_mail_input_test(self):
        self.driver.switch_to.frame("authIframe")
        self.logger.info("Ввод почтового адреса тестового аккаунта")
        self.enter_text(self.mail_input, Data.Test_Login)


    @allure.step("Нажатие кнопки 'Войти или создать'")
    def click_button_login_or_create(self):
        self.logger.info("Выполняется нажатие кнопки 'Войти или создать'")
        self.click_element(self.button_log_in)

    @allure.step("Проверка корректности почты учетной записи")
    def check_corect_mail(self):
        self.logger.info(f"Проверка, что почта учетной записи соответствует ожидаемой: {Data.Test_Login}")
        self.check_text_message(self.info_email, Data.Test_Login)

    @allure.step("Проверка корректности ФИО учетной записи")
    def check_corect_name(self):
        self.logger.info(f"Проверка, что ФИО учетной записи соответствует эталонному значению: {self.corect_name}")
        self.check_text_message(self.info_name, self.corect_name)

    @allure.step("Ввод верного пароля администратора")
    def enter_pas_input_admin(self):
        self.logger.info("Ввод верного пароля администратора")
        self.find_element(self.pas_input).send_keys(Data.ADMIN_PASS)

    @allure.step("Ввод верного пароля тестового пользователя")
    def enter_pas_input_test(self):
        self.logger.info("Ввод верного пароля тестового пользователя")
        self.find_element(self.pas_input).send_keys(Data.Test_Pass)

    @allure.step("Нажатие кнопки 'Продолжить как...', при первом входе")
    def click_continue_after_pass_on(self):
        self.logger.info("Выполняется нажатие кнопки 'Продолжить как...', после ввода пароля")
        self.click_element(self.button_continue_as)

    @allure.step("Нажатие кнопки 'Продолжить как...', при подтверждении почты")
    def click_continue_as(self):
        self.logger.info("Выполняется нажатие кнопки 'Продолжить как...', при подтверждении почты")
        self.click_element(self.button_continue_as_afte_login)
        self.make_screenshot("Продолжить как при подтверждении почты")

    @allure.step("Проверка ошибки при входе без приглашения")
    def check_err_login_without_invitation(self):
        self.logger.info("Проверка ошибки при входе без приглашения")
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.check_text_message(self.error_login_dev, "Вход невозможен без приглашения в данный экземпляр")

    @allure.step("Нажатие кнопки 'Подтвердить'")
    def click_pas_confirm(self):
        self.logger.info("Выполняется нажатие кнопки 'Подтвердить'")
        self.click_element(self.сonfirm)

    @allure.step("Получение и ввод кода подтверждения из почты админа")
    def tu_fa_admin(self):
        verification_code = self.get_msg("imap.beget.com",self.email_address, self.password)
        self.logger.info("Получен код подтверждения из почты админа. Выполняется ввод в поле.")
        self.enter_text(self.cod_mail, verification_code)


    @allure.step("Получение и ввод кода подтверждения из почты тестового пользователя")
    def tu_fa_test(self):
        verification_code = self.get_msg("imap.beget.com", Data.Test_Login, Data.Test_Pass)
        self.logger.info("Получен код подтверждения из почты тестового пользователя. Выполняется ввод в поле.")
        self.enter_text(self.cod_mail, verification_code)
#------------------------------------готовые-шаги-для-тестов----------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
    @allure.step("Проверка первого входа Администратора с 2FA и верными данными DEV")
    def login2fa_admin_first_try_dev(self):
        self.click_login_via_Steos()
        self.enter_mail_input_admin()
        self.click_button_login_or_create()
        self.enter_pas_input_admin()
        self.click_continue_after_pass_on()
        self.tu_fa_admin()
        self.click_pas_confirm()

    @allure.step("Проверка первого входа Тестовый аккуант с 2FA и верными данными DEV")
    def login2fa_test_first_try_dev(self):
        self.click_login_via_Steos()
        self.enter_mail_input_test()
        self.click_button_login_or_create()
        self.enter_pas_input_test()
        self.click_continue_after_pass_on()
        self.tu_fa_test()
        self.click_pas_confirm()

    @allure.step("Проверка входа тестового аккаунта с верными данными, при уже успешном входе ранее, без 2fa")
    def login_test_after_login(self):
        self.click_login_via_Steos()
        self.driver.switch_to.frame("authIframe")
        time.sleep(3)
        self.check_corect_mail()
        self.check_corect_name()
        self.click_continue_as()

    @allure.step("Проверка входа тестового аккаунта с верными данными, при уже успешном входе ранее, c 2fa")
    def login_test_2fa_after_login(self):
        self.click_login_via_Steos()
        self.driver.switch_to.frame("authIframe")
        self.click_continue_as()
        self.tu_fa_test()
        self.click_pas_confirm()
#--------------------------------------------------------------------------------------------------------------
#--------страница регистрации----------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
    name = (By.CSS_SELECTOR, ".registration__field:nth-child(1) input")
    last_name = (By.CSS_SELECTOR, ".registration__field:nth-child(2) > .registration__field input")
    second_name = (By.CSS_SELECTOR, ".registration__field:nth-child(3) input")
    login = (By.CSS_SELECTOR, ".input__container:nth-child(2) > input")
    gender = (By.CSS_SELECTOR, "div:nth-child(2) .selected__container")
    men_gender = (By.ID, "2")
    women_gender = (By.ID, "1")  # Если это простой класс, можно оставить CLASS_NAME
    mail = (By.CSS_SELECTOR, ".registration__field:nth-child(6) input")
    password_autho = (By.CSS_SELECTOR, ".registration__field:nth-child(7) .have__right-icon")
    password_confirmation = (By.CSS_SELECTOR, ".registration__field:nth-child(8) .have__right-icon")
    invalid_name = (By.CSS_SELECTOR, ".registration__field:nth-child(1) .error-msg")  # Имя неверного формата
    invalid_last_name = (By.CSS_SELECTOR,".registration__field:nth-child(2) > .validate-wrapper-error .error-msg")  # Фамилия неверного формата
    invalid_second_name = (By.CSS_SELECTOR, ".registration__field:nth-child(3) .error-msg")  # Отчество неверного формата
    invalid_password_autho = (By.CSS_SELECTOR, ".registration__field:nth-child(7) .error-msg")  # Пароль не соответствует требованиям
    invalid_password_confirmation = (By.CSS_SELECTOR, ".registration__field:nth-child(8) .error-msg")  # Пароли не совпадают
    save = (By.CSS_SELECTOR, ".color-type__primary")

    @allure.step("Проверка ввода коректного имени")
    def enter_name(self):
        self.logger.info("Ввод корректного имени")
        self.input_credentials(self.name, "VoicenameNAME")

    @allure.step("Проверка ввода неверного имени и проверка отсутствия ошибки")
    def enter_err_name(self):
        self.logger.info("Ввод некорректного имени")
        self.input_credentials(self.name, "Test_name")
        err_el = self.find_element(self.invalid_name)
        if err_el.is_displayed():
            self.check_text_message(self.invalid_name, "Имя неверного формата")
            self.logger.error("Ошибка при вводе имени")
        else:
            self.logger.info("Ошибки при вводе имени не обнаружено.")

    @allure.step("Проверка ввода фамилии")
    def enter_last_name(self):
        self.logger.info("Ввод корректной фамилии")
        self.input_credentials(self.last_name, "VoiceLastname")

    @allure.step("Проверка ввода некоректной фамилии и проверка отсутствия ошибки")
    def enter_ERR_last_name(self):
        self.logger.info("Ввод некоректной фамилии и проверка отсутствия ошибки")
        self.input_credentials(self.last_name, "Test_last_name")
        err_el = self.find_element(self.invalid_last_name)
        if err_el.is_displayed():
            self.check_text_message(self.invalid_last_name, "Фамилия неверного формата")
            self.logger.error("Ошибка при вводе фамилии")
        else:
            self.logger.info("Ошибки при вводе фамилии не обнаружено.")

    @allure.step("Проверка ввода отчества")
    def enter_second_name(self):
        self.logger.info("Ввод корректного отчества")
        self.input_credentials(self.second_name,"VoiceSecondName")

    @allure.step("Проверка некорректного отчества и проверка отсутствия ошибки")
    def enter_ERR_second_name(self):
        self.logger.info("Ввод некорректного отчества и проверка отсутствия ошибки")
        self.click_element(self.second_name)
        self.enter_text(self.second_name, "Test_second_name")
        err_el = self.find_element(self.invalid_second_name)
        if err_el.is_displayed():
            self.check_text_message(self.invalid_second_name, "Отчество неверного формата")
            self.logger.error("Ошибка при вводе отчества")
        else:
            self.logger.info("Ошибки при вводе отчества не обнаружено.")

    @allure.step("Проверка ввода логина")
    def enter_login(self):
        self.logger.info("Ввод корректного логина")
        self.enter_text(self.login, "oiqjwffffffffoqwdiwqudhuqwbuy1g22gudu1i2u")

    @allure.step("Проверка выбора пола")
    def select_gender(self):
        self.logger.info("Выбор пола: женский")
        self.click_element(self.gender)
        self.click_element(self.women_gender)

    @allure.step("Проверка ввода паролей")
    def input_pass_author(self):
        self.logger.info("Ввод корректных паролей в поля 'пароль' и 'подтверждение пароля'")
        self.find_element(self.password_autho).send_keys(Data.Test_Pass)
        self.find_element(self.password_confirmation).send_keys(Data.Test_Pass)

    @allure.step("Проверка ввода некорректного пароля и проверка сообщения об ошибке")
    def enter_ERR_pass_autho(self):
        self.logger.info("Ввод некорректного пароля и проверка сообщения об ошибке")
        self.input_credentials(self.password_autho, "123")
        err_el = self.find_element(self.invalid_password_autho)
        if err_el.is_displayed():
            expected_message = "Пароль не соответствует требованиям. Убедитесь, что пароль содержит:\n" \
                               "– от 8 до 64 символов\n" \
                               "– хотя бы одну заглавную и одну строчную букву\n" \
                               "– хотя бы одну цифру\n" \
                               "– только допустимые специальные символы:\n" \
                               "~!?@#$%^&*_-+()[]{}></\\|'\",:."
            self.logger.error("Ошибка при вводе пароля: " + expected_message)
        else:
            self.logger.info("Ошибки при вводе пароля не обнаружено.")

    @allure.step("Проверка ввода некоректного пароля и проверка отсутствия ошибки")
    def enter_ERR_pass_confirmation(self):
        self.logger.info("Ввод некоректной фамилии и проверка отсутствия ошибки")
        self.input_credentials(self.password_confirmation, "123")
        err_el = self.find_element(self.invalid_password_confirmation)
        if err_el.is_displayed():
            self.check_text_message(self.invalid_password_confirmation, "Пароли не совпадают")
            self.logger.error("Ошибка при вводе подтверждения пароля")
        else:
            self.logger.info("Ошибки при вводе подтверждения пароля не обнаружено.")

    @allure.step("Проверка нажатия кнопки 'Сохранить'")
    def save_click(self):
        self.logger.info("Нажатие кнопки 'Сохранить'")
        self.click_element(self.save)

    @allure.step("Проверка состояния кнопки 'Сохранить'")
    def is_save_button_disabled(self):
        self.logger.info("Проверка состояния кнопки 'Сохранить'")
        button = self.find_element(self.save)
        if button.get_attribute("disabled"):
            self.logger.info("Кнопка 'Сохранить' неактивна")
            return True
        else:
            self.logger.info("Кнопка 'Сохранить' активна")
            return False

    @allure.step("Проверка отсутствия возможности нажатия кнопки 'Сохранить'")
    def check_save_not_clickeble(self):
        self.logger.info("Проверка отсутствия возможности нажатия кнопки 'Сохранить'")
        err_el = self.find_element(self.save)
        if err_el.is_displayed():
            self.logger.error("Ошибка при нажатии кнопки 'Сохранить'")
        else:
            self.logger.info("Отсутствие возможности нажатия кнопки 'Сохранить' не обнаружено.")

    @allure.step("Ввод почтового адреса для нового пользователя")
    def enter_mail_input_create(self):
        self.driver.switch_to.frame("authIframe")
        self.logger.info("Ввод почтового адреса для нового пользователя")
        self.enter_text(self.mail_input, Data.Test_Login)

    @allure.step("Ввод почтового адреса для проверок страницы логина")
    def enter_mail_input_create_from_ERR_test_login(self):
        self.driver.switch_to.frame("authIframe")
        self.logger.info("Ввод почтового адреса для нового пользователя")
        self.enter_text(self.mail_input, 'error@mail.ru')

    @allure.step("Ввод пароля нового пользователя после создания")
    def enter_pas_input_after_create(self):
        self.logger.info("Ввод пароля нового пользователя после создания")
        self.find_element(self.pas_input).send_keys(Data.Test_Pass)

# ------------------------------------готовые-шаги-для-тестов----------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

    @allure.step("Создание аккаунта с корректными данными без 2fa")
    def corect_create_test_user(self):
        self.logger.info("Запуск процесса создания аккаунта с корректными данными без 2fa на voice")
        self.click_login_via_Steos()
        self.enter_mail_input_create()
        self.click_button_login_or_create()
        self.enter_name()
        self.enter_second_name()
        self.enter_last_name()
        self.enter_login()
        self.input_pass_author()
        self.save_click()
        self.enter_pas_input_after_create()
        self.click_continue_after_pass_on()

    @allure.step("Создание аккаунта с корректными данными с 2fa")
    def corect_create_test_user_w2fa(self):
        self.logger.info("Запуск процесса создания аккаунта с корректными данными без 2fa на voice")
        self.click_login_via_Steos()
        self.enter_mail_input_create()
        self.click_button_login_or_create()
        self.enter_name()
        self.enter_second_name()
        self.enter_last_name()
        self.enter_login()
        self.input_pass_author()
        self.save_click()
        self.enter_pas_input_after_create()
        self.click_continue_after_pass_on()
        self.tu_fa_test()
        self.click_pas_confirm()

    @allure.step("Создание аккаунта с некорректными данными")
    def ERR_create(self):
        self.logger.info("Запуск процесса создания аккаунта с некорректными данными")
        self.click_login_via_Steos()
        self.enter_mail_input_create_from_ERR_test_login()
        self.click_button_login_or_create()
        self.enter_err_name()
        self.enter_ERR_second_name()
        self.enter_ERR_last_name()
        self.enter_login()
        self.enter_ERR_pass_autho()
        # self.enter_ERR_pass_confirmation()
        self.is_save_button_disabled()

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------SQL---------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
    @allure.step("Удаление аккаунта из Базы данных Steos")
    def delete_from_STEOS(self, db_name="Steos", email="test123@steos.io"):
        self.logger.info("Удаление аккаунта из Базы данных Steos")
        self.logger.info(f"Поиск person_id в таблице 'contacts' для email: {email}")
        user_id = self.get_user_id_from_contacts(db_name, email)
        if user_id:
            self.logger.info(f"Найден person_id: {user_id}")
            self.delete_person_STEOS(db_name, user_id)
            self.logger.info(f"Удален пользователь с email '{email}'")
        else:
            self.logger.error(f"Пользователь с email '{email}' не найден в бд {db_name}.")

    @allure.step(f"Удаление аккаунта из Базы данных Voice")
    def delete_personal_data_voice(self,db_name="Voice", email="test123@steos.io"):
        self.logger.info(f"Удаление аккаунта из Базы данных {db_name}]")
        self.logger.info(f"Поиск person_id в таблице 'company.cmp_contacts' для email: {email}")
        person_id = self.get_person_id_from_cmp_contacts(db_name, email)
        if person_id:
            self.logger.info(f"Найден person_id: {person_id}")
            user_id = self.get_id_from_public_users(db_name, person_id)
            self.logger.info("Найден user_id: " + str(user_id))
            self.delete_from_public(db_name, user_id)
            self.delete_from_company_person(db_name, person_id)
            self.logger.info(f"Удален пользователь с email '{email}' из базы данных {db_name}")
        else:
            self.logger.error(f"Пользователь с email '{email}' не найден в бд {db_name}.")

    @allure.step(f"Удаление аккаунта из Базы данных Dev")
    def delete_personal_data_dev(self,db_name="Dev", email="test123@steos.io"):
        self.logger.info(f"Удаление аккаунта из Базы данных {db_name}]")
        self.logger.info(f"Поиск person_id в таблице 'company.cmp_contacts' для email: {email}")
        person_id = self.get_person_id_from_cmp_contacts(db_name, email)
        if person_id:
            self.logger.info(f"Найден person_id: {person_id}")
            user_id = self.get_id_from_public_users(db_name, person_id)
            self.logger.info("Найден user_id: " + str(user_id))
            self.delete_from_public(db_name, user_id)
            self.delete_from_company_person(db_name, person_id)
            self.logger.info(f"Удален пользователь с email '{email}' из базы данных {db_name}")
        else:
            self.logger.error(f"Пользователь с email '{email}' не найден в бд {db_name}.")

    @allure.step("Создание приглашения в Dev")
    def create_invite(self, db_name="Dev", email="test123@steos.io"):
        self.logger.info(f"Создание приглашения для пользователя {email} в бд {db_name}")
        self.create_user_invite(db_name, email)

    @allure.step("Удаление приглашения в Dev")
    def delete_invite(self, db_name="Dev", email="test123@steos.io"):
        self.logger.info(f"Удаление приглашения для пользователя {email} в бд {db_name}")
        self.delete_invitee(db_name, email)

    @allure.step("Удаление данных для проверки 2fa из Базы данных Steos")
    def delete_from_2fa_STEOS(self, db_name="Steos", email="bespaly.d.i@steos.io"):
        self.logger.info("Удаление аккаунта из Базы данных Steos")
        self.logger.info(f"Поиск person_id в таблице 'contacts' для email: {email} для удаления 2fa")
        user_id = self.get_user_id_from_contacts(db_name, email)
        if user_id:
            self.logger.info(f"Найден person_id: {user_id}")
            self.delete_on_steos_for_2fa(db_name, user_id)
            self.logger.info(f"Удалены данные для проверки 2fa с email '{email}'")
        else:
            self.logger.error(f"Пользователь с email '{email}' не найден в бд {db_name} для удаления 2fa.")

    @allure.step("Удаление аккаунта из всех баз данных")
    def delete_from_all_base(self):
        self.delete_from_STEOS()
        self.delete_personal_data_dev()
        self.delete_personal_data_voice()
        self.delete_invite()
        self.close_db_connections()