from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement

# Added for FireFox support
from webdriver_manager.firefox import GeckoDriverManager
import chromedriver_autoinstaller

import os
import time

def retry(func):
    """
    Adds retry functionality to functions
    """
    # wrapper function
    def wrapper(*args, **kwargs):
        max_tries = 5
        attempt = 1
        status = False
        while not status and attempt < max_tries:
            print(f'[{func.__name__}]: Attempt - {attempt}')
            status = func(*args, **kwargs)
            if status == 'skip_retry':
                status = False
                break                    
            attempt +=  1
        return status
    return wrapper


class Insta:
    def __init__(self, username, password, timeout=30, browser='chrome', headless=False):
        # current working directory/driver
        #install chroem driver if not exist
        chromedriver_autoinstaller.install()

        self.browser = 'chrome'
        self.driver_baseloc = os.path.join(os.getcwd(), 'driver')
        self.comment_disabled = False

        # Firefox
        if browser.lower() == 'firefox':
            self.browser = 'firefox'
            # Firefox Options
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.set_preference("dom.webnotifications.enabled", False)
            options.log.level = 'fatal'

            # current working directory/driver/firefox
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager(path=os.path.join(self.driver_baseloc, 'firefox')).install(),
                options=options)
        # Chrome
        else:
            # Chrome Options
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--disable-notifications")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--log-level=3")
            options.add_argument("--start-maximized")

            # current working directory/driver/chrome
            self.driver = webdriver.Chrome(options=options)
                
            # self.driver = webdriver.Chrome(
            #     executable_path="C:\chromedriver_win32\chromedriver.exe",
            #     options=options)

        self.wait = WebDriverWait(self.driver, timeout)
        self.baseurl = "https://www.instagram.com"
        self.targeturl = self.baseurl
        self.username = username
        self.password = password
        self.tag = None
        self.account = None

    def dont_save_login_info(self):
        """
        Clicks 'Not Now' button when prompted with 'Save Your Login Info?'
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, '._acan._acao._acas button'))).click()
            return True
        except:
            return False

    def login(self):
        """
        Initiates login with username and password
        """
        try:
            self.driver.get(self.baseurl)
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Log In"]'))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]'))).send_keys(self.username)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(self.password)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
        except:
            return False
        return True

    def validate_login(self):
        """
        Validates login
        """
        try:
            # look for user avatar
            self.wait.until(EC.presence_of_element_located((By.ID, 'f148b0325c55d1')))
            return True
        except:
            return False

    def is_page_loaded(self):
        """
        Checks if page is loaded successfully
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            return True
        except:
            return False

    def fetch_userAgent(self):

        try:
            user_agent= self.driver.execute_script("return navigator.userAgent")
            return user_agent
        except:
            return False

    def get_cookie(self):
        try:
            self.driver.get('https://www.instagram.com/tanlalana.farm/')
            cookie = self.driver.get_cookies()

            return cookie
        except:
            return False


    def btn_search(self):
        """
        Clicks 'Not Now' button when prompted with 'Save Your Login Info?'
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, '//*[@id="mount_0_0_S9"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/a/div/div[1]/div/div'))).click()
            return True
        except:
            return False
