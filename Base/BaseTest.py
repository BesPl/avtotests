import pytest

from Pages.LoginPage.login_steos import LoginSteos
from Pages.DEV.MainPage.MainPagePy import MainDev
from Pages.DEV.MainPage.Dev_Login import Dev_Login
from Pages.VOICE.Voice_Login import Voice
from Pages.VOICE.MainVoice import MainVoice
from logger_all import setup_logger
from config.data import Data


class BaseTest:
    login_steos = LoginSteos
    DEV_main_page = MainDev
    VOICE_main = MainVoice
    Dev_Login = Dev_Login
    data = Data
    voice = Voice

    # Основной setup для всех тестов
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.data = Data
        self.VOICE_main = MainVoice(driver)
        self.voice = Voice(driver)
        self.DEV_main_page = MainDev(driver)
        self.Dev_Login = Dev_Login(driver)
        self.login_steos = LoginSteos(driver)
        self.logger = setup_logger(self.__class__.__name__)

    # Специальный setup для тестов с изолированным драйвером
    @pytest.fixture
    def isolated_setup(self, request, driver, isolated_driver):
        self.driver = driver
        self.data = Data
        self.VOICE_main = MainVoice(driver)
        self.voice = Voice(driver)
        self.DEV_main_page = MainDev(driver)
        self.Dev_Login = Dev_Login(driver)
        self.login_steos = LoginSteos(driver)

        self.isolated_driver = isolated_driver
        self.isolated_VOICE_main = MainVoice(isolated_driver)
        self.isolated_voice = Voice(isolated_driver)
        self.isolated_DEV_main_page = MainDev(isolated_driver)
        self.isolated_Dev_Login = Dev_Login(isolated_driver)
        self.isolated_login_steos = LoginSteos(isolated_driver)

        self.logger = setup_logger(self.__class__.__name__)
        return self