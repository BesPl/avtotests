import pytest
import allure
from BaseTest import BaseTest


@allure.feature("Profile Functionality")
class TestProfileFeature(BaseTest):


    @allure.title("login")
    @allure.severity("Critical")
    @pytest.mark.smoke
    def test_google_search(self):
        self.login_page.open()
        self.login_page.is_opened()
        self.login_page.google_search()
