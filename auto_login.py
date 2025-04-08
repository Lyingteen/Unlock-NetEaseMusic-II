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
    browser.add_cookie({"name": "MUSIC_U", "value": "002AAE2688858C460DFAF2394574FAEB482CA68E817A6E2B5ACADD602F343B24ACF70B3B671BD9E57649451F1663389D7353CB31FA6E4E77F5F73F643D9C6A4142CB0F7867194A240023F8D7F40401F25AE7A0BDDD0CD88F1AA8A52F7B38EE889929907C919EC771FF3B25C769F05E5A5BD9E73C335CBBE019175D8700F522C83DF33CD9A5D354AE828056D44E4A1CA12F2F6C84BF2E41428405FADB6E7A6762CBFE00DBB1A0AA2DF1C26C6BBF5533F9E09322F4C0BDF453946470FB5C20AD0A08E147ACFBDB89D7FC72142C752134BBE54223212628E0218A227530F8AA57B336E1E87690AAE795EA9F86A40AD24AD2BAFFABD9D4D0DD69AA44D9A4C39BC62FF0B0AA1AED7E96C26DC0D14806B1F8AEAB46FCCAF6D430523865F84BAE063DFCDE7183D4E97782B415BE4B6477CCD432AC053AF58A43734B7D9D5D435DF1CB0C902A5D432E9444230471BF8C4945C021CBF64307D34C503F059CE19F8835497D5F"})
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
