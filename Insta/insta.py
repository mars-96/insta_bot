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


class InstaBot:
    def __init__(self, browser) -> None:
        self.browser=browser

        # Initialize resources and return
        if self.browser == "chrome":
            driver = webdriver.Chrome(ChromeDriverManager().install())
        elif self.browser == "firefox":
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        else:
            raise ValueError("Invalid browser name")
        self.driver = driver
        self.URL="https://www.instagram.com/accounts/login/"
        # return self.driver
    def __enter__(self):
        return self
    # Navigate to the Instagram login page
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def get_url(self):
        self.driver.get(self.URL)

    # Enter your login credentials and click the login button
    def login(self):
        username_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        password_input = self.driver.find_element(By.NAME, "password")

        # Enter your credentials and submit the form
        username_input.send_keys("usama.khan.codedesk@gmail.com")
        password_input.send_keys("Admin#125")
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
        
        sleep(3)
        STORY_URL = "https://instagram.com/stories/uarhamsoft/3053908816545589341?utm_source=ig_story_item_share&igshid=MDJmNzVkMjY="
        self.driver.get(STORY_URL)
        sleep(3)

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
            next_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Next']"))
            )
            
            while next_button.is_displayed():
                sleep(5)
                next_button.click()
        except TimeoutException:
            print("Not found next")
                
        sleep(50)

        # driver.get("https://www.instagram.com/stories/username/story-id/")

        # View the story by clicking through it
        # sleep(5)
        # next_button = driver.find_element_by_css_selector("button[class='coreSpriteRightChevron']")
        # while next_button.is_displayed():
        #     next_button.click()
        #     sleep(2)

        # Close the browser window
