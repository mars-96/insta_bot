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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


class Credentials(BaseModel):
    email: str
    password: str


class InstaBot:
    def __init__(self, browser, credentials_file, proxy_file="proxies.csv") -> None:
        self.browser = browser
        self.credentials_file = credentials_file

        # Initialize resources and return

        self.URL = "https://www.instagram.com/accounts/login/"
        # self.URL = "https://www.google.com/"
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
            rand_proxy = random.choice(self.proxies)
            # proxy=f'{rand_proxy.get("ip")}:{rand_proxy.get("port")}'
            # proxy = f"103.149.146.34:80"

            # breakpoint()
            # webdriver.DesiredCapabilities.CHROME["proxy"] = {
            #     "httpProxy": proxy.get("ip"),
            #     "ftpProxy": proxy.get("ip"),
            #     "sslProxy": proxy.get("ip"),
            #     "proxyType": "MANUAL",
            # }
        # breakpoint()
        if self.browser == "chrome":
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument(f'--proxy-server={rand_proxy.get("ip")}:{rand_proxy.get("port")}')
            try:
                # Try to create a Chrome driver instance
                driver = webdriver.Chrome(options=chrome_options)
            except:
                ChromeDriverManager().install()
                driver = webdriver.Chrome(options=chrome_options)
            # chrome_options.add_argument(f'--proxy-server=103.145.113.78:80')
            # driver = webdriver.Chrome(
            #     ChromeDriverManager().install(), options=chrome_options
            # )
        elif self.browser == "firefox":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument(f'--proxy-server={rand_proxy.get("ip")}:{rand_proxy.get("port")}')
            driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install(), options=firefox_options
            )
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
        # username_input.clear()
        # password_input.clear()
        ActionChains(self.driver).move_to_element(username_input).click().key_down(Keys.END).key_down(Keys.SHIFT).send_keys(Keys.HOME).key_up(Keys.SHIFT).key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE).perform()
        ActionChains(self.driver).move_to_element(password_input).click().key_down(Keys.END).key_down(Keys.SHIFT).send_keys(Keys.HOME).key_up(Keys.SHIFT).key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE).perform()

        sleep(1)
        # Enter your credentials and submit the form
        username_input.send_keys(credentials.email)
        password_input.send_keys(credentials.password)
        password_input.submit()
        sleep(5)
        
        credentials_error = None 
        try:
            credentials_error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "slfErrorAlert"))
            )
        except TimeoutException:
            print("Not found error")
        
        return False if credentials_error else True

    def story_view(self, story_url, username):
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

        sleep(3)
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

        sleep(random.randint(5, 10))
        # STORY_URL = "https://instagram.com/stories/uarhamsoft/3053908816545589341?utm_source=ig_story_item_share&igshid=MDJmNzVkMjY="
        print(f">>>>>>{story_url}")
        self.driver.get(story_url)
        sleep(random.randint(5, 10))

        try:
            story_prompt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button"))
            )

            # not_now_button = driver.find_element_by_xpath(".//button[text()='Not Now']")
            story_prompt.click()

        except TimeoutException:
            print("Not found Story")
        # Wait for the page to load and navigate to the first story

        try:
            # next_button = WebDriverWait(self.driver, 10).until(
            #     EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Next']"))
            # )
            
            while True:
                sleep(5)
                try:
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Next']"))
                    )
                    next_button.click()
                except TimeoutException:
                    print("Not found next")
                    break
                except StaleElementReferenceException:
                    # re-try locating the next button
                    pass
        except KeyboardInterrupt:
            print("Interrupted by user")
        
        sleep(random.randint(5, 10))
        self.driver.get(f"https://www.instagram.com/{username}")
        sleep(random.randint(5, 10))
        try:
            menu = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button._abl-"))
            )
            menu.click()
            
            logout_button = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "button:nth-of-type(10)"))
                )
            logout_button.click()
        except TimeoutException:
            print("Not found menu")
        
        sleep(random.randint(5, 10))
        # self.driver.get(self.URL)
                
        # sleep(20)
        #     print("Not found next")

        # sleep(50)
