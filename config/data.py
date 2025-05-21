import os
from dotenv import load_dotenv
# Allure plugin надо скачать
load_dotenv()

class Data:

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASS = os.getenv("ADMIN_PASS")
    ADMIN_Mail_PASS = os.getenv("ADMIN_Mail_PASS")
    Test_Login = os.getenv("Test_Login")
    Test_Pass = os.getenv("Test_Pass")
    bd_host = os.getenv("bd_host")
    bd_login = os.getenv("bd_login")
    bd_pwd = os.getenv("bd_pwd")
    bd_st_vs_host = os.getenv("bd_st_vs_host")
    bd_st_vs_login = os.getenv("bd_st_vs_login")
    bd_st_vs_pwd = os.getenv("bd_st_vs_pwd")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("chat_id")