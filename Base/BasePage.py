#BasePage
import time
import allure
import os
from logger_all import setup_logger
from datetime import datetime
from allure_commons.types import AttachmentType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from imap_tools import MailBox
from config.db_connections import DatabaseHelper
import re


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10, poll_frequency=1)
        self.logger = setup_logger(self.__class__.__name__)
        self.db_connections = {}



    def open(self):
        """Открывает страницу и проверяет, что она успешно загружена."""
        with allure.step(f"Открытие {self.PAGE_URL} страницы"):
            self.driver.get(self.PAGE_URL)
            self.logger.info(f"Открытие {self.PAGE_URL} страницы")
            try:
                self.wait.until(EC.url_to_be(self.PAGE_URL))
                self.logger.info(f"Страница успешно открыта: {self.PAGE_URL}")
            except Exception as e:
                self.logger.error(f"Ошибка при открытии страницы: {str(e)}")
                self.logger.error(f"Текущий URL: {self.driver.current_url}")
                raise AssertionError(
                    f"Страница {self.PAGE_URL} не была открыта. Текущий URL: {self.driver.current_url}"
                )

    def is_opened(self):
        """Проверяет, что страница открыта (дополнительная проверка)."""
        with allure.step(f"Проверка открытия страницы {self.PAGE_URL}"):
            try:
                self.wait.until(EC.url_to_be(self.PAGE_URL))
                self.logger.info(f"Страница успешно открыта: {self.PAGE_URL}")
            except Exception as e:
                self.logger.error(f"Ошибка при проверке открытия страницы: {str(e)}")
                self.logger.error(f"Текущий URL: {self.driver.current_url}")
                raise AssertionError(
                    f"Страница {self.PAGE_URL} не была открыта. Текущий URL: {self.driver.current_url}"
                )

    def is_not_opened(self):
        """Проверяет, что страница не открыта."""
        with allure.step(f"Проверка, что страница {self.PAGE_URL} не открыта"):
            try:
                self.wait.until_not(EC.url_to_be(self.PAGE_URL))
                self.logger.info(f"Страница {self.PAGE_URL} не открыта")
            except Exception as e:
                self.logger.error(f"Ошибка при проверке, что страница не открыта: {str(e)}")
                self.logger.error(f"Текущий URL: {self.driver.current_url}")
                raise AssertionError(
                    f"Страница {self.PAGE_URL} должна была быть закрыта, но осталась открытой. Текущий URL: {self.driver.current_url}"
                )

    def find_element(self, locator, timeout=10):
        """Ожидает появление элемента и возвращает его"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator),
                message=f"Элемент {locator} не найден за {timeout} секунд"
            )
        except Exception as e:
            self.logger.error(f"Ошибка поиска элемента {locator}: {e}")
            raise

    def enter_text(self, locator, text):
        """
        Очищает поле и вводит текст.
        Если элемент не найден, выбрасывает исключение.
        """
        try:
            element = self.find_element(locator)
            if element is None:
                raise Exception(f"Элемент с локатором {locator} не найден на странице.")

            element.clear()
            element.send_keys(text)
            self.logger.info(f"Введено: '{text}' в элемент {locator}")
        except Exception as e:
            self.logger.error(f"Ошибка при вводе текста в элемент {locator}: {e}")
            raise

    def click_element(self, locator):
        """Кликает на элемент после проверки его кликабельности"""
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не кликабелен"
        )
        element.click()
        self.logger.debug(f"Клик выполнен: {locator}")

    def make_screenshot(self, screenshot_name):
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{screenshot_name}_{timestamp}.png"
        file_path = os.path.join(screenshots_dir, file_name)

        self.driver.save_screenshot(file_path)

        with open(file_path, "rb") as screenshot_file:
            allure.attach(
                body=screenshot_file.read(),
                name=screenshot_name,
                attachment_type=AttachmentType.PNG
            )

    def refresh(self):
        """Обновляет страницу и проверяет её загрузку"""
        self.logger.info("Выполняю обновление страницы")
        self.driver.refresh()

        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.logger.info("Страница успешно обновлена")

    def input_credentials(self, field_locator, value):
        self.click_element(field_locator)
        self.enter_text(field_locator, value)

    def check_text_message(self, locator, expected_text):
        """
        Проверяет текст элемента.
        :param locator: Локатор элемента (например, (By.CLASS_NAME, "error-message-container"))
        :param expected_text: Ожидаемый текст для сравнения
        """
        try:
            text_element = self.find_element(locator)
            actual_text = text_element.text

            assert actual_text == expected_text, \
                f"Ожидалось сообщение '{expected_text}', но получено '{actual_text}'"

            self.logger.info(f"Текст корректный: '{actual_text}'")
        except AssertionError as e:
            self.logger.error(f"Ошибка проверки текста: {e}")
            self.logger.error(f"Фактический текст: '{actual_text}'")
            raise

    def get_msg(self, email_url, email_name: str, email_password: str) -> str:
        regex = r"\d{6}"

        self.logger.info(f"Подключение к IMAP-серверу: {email_url}")
        time.sleep(5)
        try:
            with MailBox(email_url, 993).login(email_name, email_password, 'INBOX') as mailbox:
                for msg in mailbox.fetch(limit=1, reverse=True):
                    body = msg.text
                    self.logger.debug(f"Текст письма: {body[:100]}...")

                    codes = re.findall(regex, body)
                    if codes:
                        code = codes[0]
                        self.logger.info(f"Код успешно найден: {code}")
                        return code
                    else:
                        self.logger.warning("Шестизначный код не найден в тексте письма.")
                        return None
        except Exception as e:
            self.logger.error(f"Ошибка при получении кода из письма: {e}")
            raise

    def connect_to_db(self, db_name):
        if db_name not in self.db_connections:
            try:
                self.logger.info(f"Попытка подключения к БД: {db_name}")
                conn = DatabaseHelper.get_db_connection(db_name)
                self.db_connections[db_name] = conn
                self.logger.info(f"Успешное подключение к БД: {db_name}")
                return conn
            except Exception as e:
                self.logger.error(f"Ошибка подключения к БД {db_name}: {e}")
                raise
        else:
            self.logger.info(f"Используется существующее подключение к БД: {db_name}")
            return self.db_connections[db_name]

    def execute_query(self, db_name, query, params=None):
        """
        Выполнение SQL-запроса.
        :param db_name: Имя базы данных.
        :param query: SQL-запрос.
        :param params: Параметры запроса.
        :return: Результат выполнения запроса.
        """
        self.logger.info(f"Выполняется запрос к БД {db_name}: {query} с параметрами: {params}")
        with self.connect_to_db(db_name) as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params or ())
                    if query.strip().upper().startswith("SELECT"):
                        result = cursor.fetchall()
                        self.logger.info(f"Запрос вернул {len(result)} записей.")
                        return result if result else []
                    else:
                        conn.commit()
                        self.logger.info(f"Запрос выполнен успешно: {query}")
            except Exception as e:
                self.logger.error(f"Ошибка выполнения запроса: {e}")

    def close_db_connections(self):
        """
        Закрытие всех подключений к БД.
        """
        for db_name, conn in self.db_connections.items():
            try:
                conn.close()
                self.logger.info(f"Подключение к БД {db_name} успешно закрыто.")
            except Exception as e:
                self.logger.error(f"Ошибка при закрытии подключения к БД {db_name}: {e}")

    def get_user_id_from_contacts(self, db_name, email):
        """
        Получает user_id из таблицы contacts по email.
        :param db_name: Имя базы данных.
        :param email: Электронная почта для поиска.
        :return: user_id или None, если запись не найдена.
        """
        query = """
        SELECT user_id
        FROM contacts
        WHERE value = %s
        LIMIT 1;
        """
        self.logger.info(f"Поиск user_id в таблице 'contacts' для email: {email}")
        result = self.execute_query(db_name, query, (email,))
        if result:
            user_id = result[0][0]
            self.logger.info(f"Найден user_id: {user_id} для email: {email}")
            return user_id
        else:
            self.logger.warning(f"user_id не найден для email: {email}")
            return None

    def delete_on_steos_for_2fa(self, db_name, user_id):
        self.logger.info(f"Начат процесс удаления данных для проверки 2fa: {user_id}")
        queries = [
            "DELETE FROM sessions WHERE user_id = %s;",
            "DELETE FROM twofa WHERE user_id = %s;",
            ]
        try:
            for query in queries:
                self.logger.info(f"Выполняется запрос на удаление данных для 2fa: {query} для user_id: {user_id}")
                self.execute_query(db_name, query, (user_id,))
                self.logger.info(f"Успешно удалены данных для проверки 2fa из таблицы для user_id: {user_id}")

            self.logger.info(f"Данные для user_id для fa: {user_id} успешно удалены.")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при удалении данных для user_id для 2fa: {user_id}: {e}")
            return False

    def delete_person_STEOS(self, db_name, user_id):
        """
        Удаление всех данных, связанных с указанным user_id, из нескольких таблиц.
        :param db_name: Имя базы данных.
        :param user_id: ID пользователя, данные которого нужно удалить.
        :return: True, если удаление успешно, иначе False.
        """
        self.logger.info(f"Начат процесс удаления данных для user_id: {user_id}")
        queries = [
            "DELETE FROM contacts WHERE user_id = %s;",
            "DELETE FROM resourse_access WHERE user_id = %s;",
            "DELETE FROM sessions WHERE user_id = %s;",
            "DELETE FROM token_balance WHERE user_id = %s;",
            "DELETE FROM user_sessions WHERE user_id = %s;",
            "DELETE FROM twofa WHERE user_id = %s;",
            "DELETE FROM users WHERE id = %s;"
        ]

        try:
            for query in queries:
                self.logger.info(f"Выполняется запрос на удаление: {query} для user_id: {user_id}")
                self.execute_query(db_name, query, (user_id,))
                self.logger.info(f"Успешно удалены записи из таблицы для user_id: {user_id}")

            self.logger.info(f"Все данные для user_id: {user_id} успешно удалены.")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при удалении данных для user_id: {user_id}: {e}")
            return False

    def get_person_id_from_cmp_contacts(self, db_name, email):
        """
        Получает person_id из company.cmp_contacts по email.
        :param db_name: Имя базы данных.
        :param email: Электронная почта для поиска.
        :return: person_id или None, если запись не найдена.
        """
        query = """
        SELECT person_id
        FROM company.cmp_contacts
        WHERE value = %s
        LIMIT 1;
        """
        self.logger.info(f"Поиск person_id в таблице 'company.cmp_contacts' для email: {email}")
        result = self.execute_query(db_name, query, (email,))
        if result:
            person_id = result[0][0]
            self.logger.info(f"Найден person_id: {person_id} для email: {email}")
            return person_id
        else:
            self.logger.warning(f"person_id не найден для email: {email}")
            return None

    def get_id_from_public_users(self, db_name, person_id):
        """
        Получает user_id из public.users по person_id.
        :param db_name: Имя базы данных.
        :param person_id: ID персоны для поиска.
        :return: user_id или None, если запись не найдена.
        """
        query = """
        SELECT id
        FROM public.users
        WHERE person_id = %s
        LIMIT 1;
        """
        self.logger.info(f"Поиск user_id в таблице 'public.users' для person_id: {person_id}")
        result = self.execute_query(db_name, query, (person_id,))
        if result:
            user_id = result[0][0]
            self.logger.info(f"Найден user_id: {user_id} для person_id: {person_id}")
            return user_id
        else:
            self.logger.warning(f"user_id не найден для person_id: {person_id}")
            return None

    def delete_from_public(self, db_name, id):
        """
        Удаление всех данных, связанных с указанным id, из нескольких таблиц.
        :param db_name: Имя базы данных.
        :param id: ID пользователя, данные которого нужно удалить.
        :return: True, если удаление успешно, иначе False.
        """
        self.logger.info(f"Начат процесс удаления данных для user_id: {id}")
        queries = [
            "DELETE FROM public.user_settings WHERE user_id = %s;",
            "DELETE FROM public.notifications WHERE user_id = %s;",
            "DELETE FROM public.user_sessions WHERE user_id = %s;",
            "DELETE FROM public.users WHERE id = %s;"
        ]

        try:
            for query in queries:
                self.logger.info(f"Выполняется запрос на удаление: {query} для user_id: {id}")
                self.execute_query(db_name, query, (id,))
                self.logger.info(f"Успешно удалены записи из таблицы для user_id: {id}")

            self.logger.info(f"Все данные для user_id: {id} успешно удалены.")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при удалении данных для user_id: {id}: {e}")
            return False

    def delete_from_company_person(self, db_name, person_id):
        """
        Удаление всех данных, связанных с указанным person_id, из нескольких таблиц компании.
        :param db_name: Имя базы данных.
        :param person_id: ID персоны, данные которой нужно удалить.
        :return: True, если удаление успешно, иначе False.
        """
        self.logger.info(f"Начат процесс удаления данных для person_id: {person_id}")
        queries = [
            "DELETE FROM company.cmp_document_person WHERE person_id = %s;",
            "DELETE FROM company.cmp_contacts WHERE person_id = %s;",
            "DELETE FROM company.cmp_persons WHERE id = %s;"
        ]

        try:
            for query in queries:
                self.logger.info(f"Выполняется запрос на удаление: {query} для person_id: {person_id}")
                self.execute_query(db_name, query, (person_id,))
                self.logger.info(f"Успешно удалены записи из таблицы для person_id: {person_id}")

            self.logger.info(f"Все данные для person_id: {person_id} успешно удалены.")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при удалении данных для person_id: {person_id}: {e}")
            return False

    def create_user_invite(self, db_name, email):
        """
        Создаёт новую запись в таблице public.user_invites с указанными email и role_id = 1.
        :param db_name: Имя базы данных.
        :param email: Электронная почта для новой записи.
        :return: True, если создание успешно, иначе False.
        """
        query = """
        INSERT INTO public.user_invites (email, role_id) VALUES (%s, 1);
        """
        self.logger.info(f"Начат процесс создания приглашения для email: {email}")

        try:
            self.execute_query(db_name, query, (email,))
            self.logger.info(f"Приглашение для email: {email} успешно создано.")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при создании приглашения для email: {email}: {e}")
            return False

    def delete_invitee(self, db_name, email):

        self.logger.info(f"Начат процесс удаления приглашения в {db_name} для person_id: {email}")
        queries = [
            "DELETE FROM public.user_invites  WHERE email = %s;",
        ]

        try:
            for query in queries:
                self.logger.info(f"Выполняется запрос на удаление приглашения в {db_name}: {query} для email: {email}")
                self.execute_query(db_name, query, (email,))
                self.logger.info(f"Успешно удалены записи из таблицы для для email: {email}")

            self.logger.info(f"Приглашение для email: {email}: успешно удалено.")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при удалении приглашения для email: {email} {e}")
            return False

