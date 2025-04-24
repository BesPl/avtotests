import os
import subprocess
import sys


def run_tests():
    # Шаг 1: Запуск pytest с генерацией allure-results
    print("Запуск pytest...")
    pytest_command = ["pytest", "--alluredir=allure-results"]
    result = subprocess.run(pytest_command)

    if result.returncode != 0:
        print("Тесты завершились с ошибкой. Проверьте логи.")
        sys.exit(result.returncode)

    # Шаг 2: Выполнение cp_hist.py
    print("Выполнение cp_hist.py...")
    try:
        subprocess.run(["python", "cp_hist.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении cp_hist.py: {e}")
        sys.exit(e.returncode)

    # Шаг 3: Генерация allure-report
    print("Генерация allure-report...")
    allure_generate_command = ["allure", "generate", "allure-results", "--clean", "-o", "allure-report"]
    try:
        subprocess.run(allure_generate_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации allure-report: {e}")
        sys.exit(e.returncode)

    # Шаг 4: Открытие allure-report
    print("Открытие allure-report...")
    allure_open_command = ["allure", "open", "allure-report"]
    try:
        subprocess.run(allure_open_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при открытии allure-report: {e}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    run_tests()