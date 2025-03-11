# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0030387D8146B241740CEEC7877C22CB02712B572246BA11D0506F46A6295259E5827327A738D3A19793EDF348BC214A1A477875C59E3FD49E2BAF179741B86A70D76084CC595132878C6E41C441A718D345A733FCF643CD66B20A52BA2A1433C690B127FEAA6DFC9A5E583D3A443162399AB7E1AB591ACC4EF0F23E0B2176B28439DF9F8A7CEEA2E10226FD0DBD882E2A3A564E3F88CF20A71EF1E9A96DF4E2F7A1208443B7E07F603E787FFA146ACCE575683235C00C8542437384AB1503E1AB7340D438D703172F6CE091426CA7827CCD456F267AED5F4C88C1B98F43BA30DC90758CC36471F32C5316DAD7AADDD00DB8FEF2249E36FC2C764EC42C459EB8D1C29F834EF0C65824FD86843FA2F8B7D1FFAABE5F27544EC60470170D317012A50E14854627773F378EEEC2732C9552E15D0E53AE266119D0BB63C49E4BD4EEBB2B50E6A3EBAA748F7BB1FD30A9F3AC527554239077832DC164D4B9E1B20C7675"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
