
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_auto_update import check_driver
import json
import time
import os
import sys
import time
from retryDecorator import retry


'''

Basic script that uses Selenium to open chromium to the specified landing page and
enters a username and password in the element_username and element_password fields.

Optimized for use with crontab at reboot to simulate kiosk mode. '--kiosk' chromium
flag does not work.

'sudo apt-get install chromium-chromedriver' for ARM based chromedriver developed by
the rapsberry pi community.

'''


# Global Variables
with open(os.path.join(sys.path[0], 'orion_config.json')) as inf:
    conf = json.load(inf)
    center_page = conf['center_page']
    view_mode = conf['view_mode']
    left_page = conf['left_page']
    right_page = conf['right_page']
    user_agent = conf['user_agent']
    driver_location = conf['driver_location']
    username = conf['username']
    password = conf['password']
    element_username = conf['element_username']
    element_password = conf['element_password']
    element_placeholder = conf['element_placeholder']
inf.close()


def updateLibs():
    os.system('pip-review --auto')
    os.system('pip freeze > requirements.txt')
    check_driver(driver_location)
    return


# loads chromium-chromedriver
@retry(tries=4, delay=3, backoff=1)
def loadDriver():

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--noerrdialogs')
    options.add_argument('disable-infobars')
    options.add_argument(user_agent)
    prefs = {"credentials_enable_service": False,
             "profile": {"password_manager_enabled": False}}
    options.add_experimental_option('prefs', prefs)
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ["enable-automation"])
    driver = webdriver.Chrome(
        service=ChromeService(
            driver_location +
            "\\chromedriver.exe"),
        options=options)

    return driver


# Enter in a username and password and hit enter
def loginOrion(driver):
    element = WebDriverWait(
        driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, element_username)))
    element.send_keys(username)

    element = driver.find_element(By.ID, element_password)
    element.send_keys(password)

    element.send_keys(Keys.RETURN)

    return


def orionViewMode(driver):
    WebDriverWait(
        driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, element_placeholder)))
    driver.get(view_mode)
    return driver


if __name__ == '__main__':
    updateLibs()
    center_driver = loadDriver()
    left_driver = loadDriver()
    right_driver = loadDriver()

    left_driver.set_window_position(-1000, 0)
    left_driver.get(left_page)
    time.sleep(0.5)
    loginOrion(left_driver)
    left_driver.fullscreen_window()

    right_driver.set_window_position(3000, 0)
    right_driver.get(right_page)
    right_driver.fullscreen_window()

    center_driver.set_window_position(0, 0)
    center_driver.get(center_page)
    time.sleep(0.5)
    loginOrion(center_driver)
    center_driver.maximize_window()
    orionViewMode(center_driver)
    center_driver.fullscreen_window()

    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        center_driver.close()
        left_driver.close()
        right_driver.close()
