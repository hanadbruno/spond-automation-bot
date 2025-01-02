import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Prevent Chrome from running in sandbox mode
chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Get credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Debugging output to check if email and password are being retrieved correctly
print(f"Email: {email}")
print(f"Password: {password}")

if not email or not password:
    raise ValueError("Email or password is missing in the environment variables.")

try:
    # Step 1: Open the Spond login page
    driver.get("https://spond.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

    # Step 2: Log in to your account
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    password_field.submit()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@name='accept-button']")))

    # Step 3: Navigate to the group event page
    driver.get("https://spond.com/client/groups/4AC9EBBFC5284E0BBB0B38760D5F2AC1")  # Example group URL

    # Step 4: Wait until the event card is available
    event_card = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='spondCardstyled__EventHeading-sc-1adg5oi-19 fmtvKb']/a"))
    )
    event_url = event_card.get_attribute("href")  # Get the event URL
    print(f"Found event: {event_url}")

    # Step 5: Extract the event date
    event_date_str = driver.find_element(By.XPATH, "//div[@class='spondCardstyled__EventStartTime-sc-1adg5oi-31 eyspoB']").text
    event_date = datetime.strptime(event_date_str, "%A %d. %b. kl. %H:%M")  # Norwegian date format
    print(f"Event date: {event_date}")

    # Step 6: Calculate the target time to wait (2 days before the event)
    target_time = event_date - timedelta(days=2)
    current_time = datetime.now()

    if current_time < target_time:
        wait_time = (target_time - current_time).total_seconds()
        print(f"Waiting for {wait_time} seconds until the target time.")
        time.sleep(wait_time)  # Wait until the event date minus 2 days

    # Step 7: Now that it's time, proceed with the action (e.g., accepting the event)
    driver.get(event_url)  # Go to the event page
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@name='accept-button' and not(@disabled)]"))
    )

    accept_button = driver.find_element(By.XPATH, "//button[@name='accept-button' and not(@disabled)]")
    accept_button.click()
    print("Successfully accepted the event!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
