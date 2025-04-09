import os
import shutil


ALLURE_RESULTS = "./allure-results"
ALLURE_REPORT = "./allure-report"
HISTORY_DIR = os.path.join(ALLURE_REPORT, "history")
TARGET_HISTORY_DIR = os.path.join(ALLURE_RESULTS, "history")



# Копирование history с заменой старой папки
if os.path.exists(HISTORY_DIR):
    # Удаление старой папки history в allure-results, если она существует
    if os.path.exists(TARGET_HISTORY_DIR):
        shutil.rmtree(TARGET_HISTORY_DIR)
    # Копирование новой папки history
    shutil.copytree(HISTORY_DIR, TARGET_HISTORY_DIR)
