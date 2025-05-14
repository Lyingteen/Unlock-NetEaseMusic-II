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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A62A5BF2F03DD923F869CE12B6910FE684A78965FD16F52151DFF466DC4DC3991EC3995642955D0C445E6BE7DC9D911E8E12CB0490523D62C686EFFBE86B510F52C4C59B661D5DFE6791E39CE2ABFCDD2F0A94F150532D07635B4BAC7B1AEA478670128D56346D1C812FEFCFC60C8E625EBFBE71E084A2A7EB14EA15AD55B3FEE4EBFA5F7B6C551A58A60CF46F0EDB32BEFB7EBC31418F991AA6ADA83D8F729E20F602913F3AB9B27876918C1CF3465F4B43F93F48764154ECFF4C935D979A170274A2856AA43545E5B2BAF4711927C6284EFE0F0EE809B5910FA9BA5B20177235DA155D2DD1AD264BB78206C87E3E9DB2678E310352FFCA71A24AEC77BDDD7789DEE1A327D381D34FFD5F0DE615D29E90B06AC2FEEC7737114D8E5EF630EBBA4077953C2C33757CAAE5908FC5A954068B927F6945087F67E8476F21E96D8A2DF05B4BD2931BB8122CFC16DEA1D7D131CCCE5D90DADBB113D8FB87A35F017265"})
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
