from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

# Replace with the path to your own webdriver
driver = webdriver.Chrome()

# Navigate to the Instagram login page
driver.get("https://www.instagram.com/accounts/login/")

# Enter your login credentials and click the login button
username_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "username"))
)
password_input = driver.find_element(By.NAME, "password")

# Enter your credentials and submit the form
username_input.send_keys("usama.khan.codedesk@gmail.com")
password_input.send_keys("Admin#125")
password_input.submit()
sleep(5)

try:
    save_info_prompt = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "main[role='main'] button._acan._acao._acas._aj1-"))
    )

    print(f"save_info_prompt:")
    save_info_prompt.click()
except TimeoutException:
    print("not found")

sleep(6)

try:
    notNow_info_prompt = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'] button:nth-of-type(2)"))
    )

    # not_now_button = driver.find_element_by_xpath(".//button[text()='Not Now']")
    notNow_info_prompt.click()
except TimeoutException:
    print("not found popup")

story_url = "https://instagram.com/stories/uarhamsoft/3053908816545589341?utm_source=ig_story_item_share&igshid=MDJmNzVkMjY="
driver.get(story_url)

try:
    story_prompt = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button"))
    )

    # not_now_button = driver.find_element_by_xpath(".//button[text()='Not Now']")
    story_prompt.click()
except TimeoutException:
    print("Not found Story")
# Wait for the page to load and navigate to the first story
sleep(50)


# driver.get("https://www.instagram.com/stories/username/story-id/")

# View the story by clicking through it
# sleep(5)
# next_button = driver.find_element_by_css_selector("button[class='coreSpriteRightChevron']")
# while next_button.is_displayed():
#     next_button.click()
#     sleep(2)

# Close the browser window
driver.quit()
