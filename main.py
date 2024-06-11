import configparser
import time
import random
import string
import threading
import sys
from pathlib import Path
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')

password = config['Settings']['password']
referral_code = config['Settings']['referral_code']
api_key = config['Settings']['api_key']

# Функции для генерации случайного имени пользователя и электронной почты
def genUserEmail(length=7):
    UserName = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return UserName + '@gmail.com'

def genUserName(length=8):
    UserName = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return UserName

def initBrowser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")

    # Добавление расширений Chrome
    chrome_options.add_argument("--load-extension=C:\\py_fast\\nodepay,C:\\py_fast\\plugin")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def start():
    driver = initBrowser()
    try:
        print()
        print("Создаем окно браузера")
        driver.get("https://app.nodepay.ai/register")

        name = genUserName()
        email = genUserEmail()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "basic_email"))).send_keys(email)
        driver.find_element(By.ID, "basic_username").send_keys(name)
        driver.find_element(By.ID, "basic_password").send_keys(password)
        driver.find_element(By.ID, "basic_confirm_password").send_keys(password)
        driver.find_element(By.ID, "basic_referral_code").send_keys(referral_code)
        driver.find_element(By.ID, "basic_agree").send_keys(Keys.SPACE)

        now1 = datetime.now() 
        current_time1 = now1.strftime("%H:%M:%S")
        print("Регистрируем. Время: ", current_time1)

        # Ожидание кликабельности кнопки и попытка клика
        try:
            WebDriverWait(driver, 600).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-btn-primary"))).click()
            print("Регистрация завершена успешно")
        except Exception as e:
            print("Ошибка при клике на кнопку регистрации:", e)
            return  # Остановка выполнения в случае ошибки

        # driver.get("chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm/index.html")
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cursor-pointer"))).click()

        # driver.switch_to.window(driver.window_handles[1])
        driver.get("https://app.nodepay.ai/login")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "basic_user"))).send_keys(name)
        driver.find_element(By.ID, "basic_password").send_keys(password)

        time.sleep(10)

        try:
            driver.find_element(By.CSS_SELECTOR, ".ant-btn-primary").click()
            print("Авторизация прошла успешно")
        except Exception as e:
            print("Ошибка при клике на кнопку авторизации:", e)
            return  # Остановка выполнения в случае ошибки

        time.sleep(3)

        driver.get("chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm/index.html")

        time.sleep(1)
        element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "img.cursor-pointer[src='/static/media/img-button-activate.596be77706adeceb8919.png']"))
        )
        element.click()
        now2 = datetime.now() 
        current_time2 = now2.strftime("%H:%M:%S")
        print("Пользователь активирован! ---------------------> Время: ", current_time2)
        time.sleep(3)
    except Exception as e:
        print("Произошла ошибка:", e)
    finally:
        driver.quit()
        time.sleep(3)

# Запуск функции start в отдельном потоке
def start_thread():
    while not stop_event.is_set():
        start()
        time.sleep(1)

# Основной цикл программы
stop_event = threading.Event()
thread1 = threading.Thread(target=start_thread)
thread1.start()

thread2 = threading.Thread(target=start_thread)
thread2.start()

thread3 = threading.Thread(target=start_thread)
thread3.start()

thread4 = threading.Thread(target=start_thread)
thread4.start()

thread5 = threading.Thread(target=start_thread)
thread5.start()
while True:
    command = input("Введите 'stop' для завершения программы: ")
    if command.strip().lower() == 'stop':
        stop_event.set()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        sys.exit(0)
