from BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pytest



class LoginPage(BasePage):
    PAGE_URL = "https://www.google.com/?hl=ru"
    asd = (By.CSS_SELECTOR, '.gLFyf')

    def google_search(self):
        self.wait.until(EC.element_to_be_clickable(self.asd)).click()
        self.logger.info("Нажата кнопка поиска")
        self.logger.debug("Это сообщение отладки")
        self.logger.info("Это информационное сообщение")
        self.logger.warning("Это предупреждение")
        self.logger.error("Это сообщение об ошибке")
        self.logger.critical("Это критическое сообщение")

