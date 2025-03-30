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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B04EB37FABF69FF5A4A026C843F9587120D546DC584A6482A4EA713DC3AD9ECCF199BF4CA518E160732A08A060A5F53BF6CF206FDE6689FFCAFF01B272081C3632E0EE8449B37D074C0904A321EA50AB4A2FF09AAF5B93D400919A4ECDD9B37627E7BF37B9FA2A23C57C3DF0212B7D92672EAAD36041ECE4831AC2EF8FCF7E8C29E916042D2FEEDDCAFA2BF75C665C08EE00ADF5647599C2D935A0A9E7A8FB0CC9A5278EBC39F48AA0C62EE0F45ADCBAEEDE7BD54B8E300C0F47ECFDED47E4563B64E08507F8C9970A2D54C49F0307287C7A8181E007EDF8D636E6A56C5C6F2E24946E6555882D7AB4134FD5EDB1FE6A7BB289B73304BE5E61F87C82832E17162B364BCA6C6522FC13D5766E518645426ADD644886674D8E373104553C9A00D64D53F9590FE5F2402E15EC66B9243DD21E36BDE34B4591D33F6D974B871C446799870B4FDBCBAB9A4BDE18E633ABF685688D30297637C9DA0A1B2BC9EFF71778"})
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
