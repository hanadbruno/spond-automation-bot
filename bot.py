import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Get credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Debugging output to check if email and password are being retrieved correctly
print(f"Email: {email}")
print(f"Password: {password}")

if not email or not password:
    raise ValueError("Email or password is missing in the environment variables.")

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Prevent Chrome from running in sandbox mode
chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage

# Set up WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

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

    # Step 3: Navigate to the event page
    driver.get("https://spond.com/your_event_url")  # Replace with your event URL

    # Step 4: Wait for the accept button and click it
    accept_button = WebDriverWait(driver, 1800).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@name='accept-button' and not(@disabled)]"))
    )
    accept_button.click()
    print("Successfully responded to the event!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
