import time

from Base.BasePage import BasePage
from config.links import Links
from selenium.webdriver.common.by import By
from config.data import Data
from selenium.webdriver.support import expected_conditions as EC
import allure


class Dev_Login(BasePage):
    PAGE_URL = Links.DEV_LOGIN