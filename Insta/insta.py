import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pydantic import BaseModel
import csv


class Credentials(BaseModel):
    email: str
    password: str


class InstaBot:
    def __init__(self, browser, credentials_file, proxy_file="proxies.csv") -> None:
        self.browser = browser
        self.credentials_file = credentials_file

        # Initialize resources and return

        self.URL = "https://www.instagram.com/accounts/login/"
        self.proxy_file = proxy_file
        self.proxies = self.get_proxies()

    def get_proxies(self):
        proxies = []
        with open(self.proxy_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                proxy = {
                    "ip": row[0],
                    "port": row[1],
                    "country": row[2],
                    "speed": row[3],
                    "type": row[4],
                    "anonymity": row[5],
                }
                proxies.append(proxy)
        return proxies

    def read_credentials(self):
        with open(self.credentials_file, "r") as f:
            for line in f:
                email, password = line.strip().split(",")
                yield Credentials(email=email, password=password)

    def __enter__(self):

        # Initialize webdriver with proxy if provided
        if self.proxies:
            proxy = random.choice(self.proxies)
            # breakpoint()
            # webdriver.DesiredCapabilities.CHROME["proxy"] = {
            #     "httpProxy": proxy.get("ip"),
            #     "ftpProxy": proxy.get("ip"),
            #     "sslProxy": proxy.get("ip"),
            #     "proxyType": "MANUAL",
            # }

        if self.browser == "chrome":
            driver = webdriver.Chrome(ChromeDriverManager().install())
        elif self.browser == "firefox":
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        else:
            raise ValueError("Invalid browser name")
        self.driver = driver

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def get_url(self):
        self.driver.get(self.URL)

    def login(self, credentials):
        username_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        password_input = self.driver.find_element(By.NAME, "password")

        # Enter your credentials and submit the form
        username_input.send_keys(credentials.email)
        password_input.send_keys(credentials.password)
        password_input.submit()
        sleep(5)

    def do_something(self):
        try:
            save_info_prompt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "main[role='main'] button._acan._acao._acas._aj1-",
                    )
                )
            )

            print(f"save_info_prompt:")
            save_info_prompt.click()
        except TimeoutException:
            print("not found")

        sleep(6)
        try:
            notNow_info_prompt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[role='dialog'] button:nth-of-type(2)")
                )
            )

            # not_now_button = driver.find_element_by_xpath(".//button[text()='Not Now']")
            notNow_info_prompt.click()
        except TimeoutException:
            print("not found popup")

        STORY_URL = "https://instagram.com/stories/uarhamsoft/3053908816545589341?utm_source=ig_story_item_share&igshid=MDJmNzVkMjY="
        self.driver.get(STORY_URL)

        try:
            story_prompt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button"))
            )

            # not_now_button = driver.find_element_by_xpath(".//button[text()='Not Now']")
            story_prompt.click()
        except TimeoutException:
            print("Not found Story")
