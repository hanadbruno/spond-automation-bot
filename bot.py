import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Get credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Set up WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Open the Spond login page
    driver.get("https://spond.com/login")
    time.sleep(2)

    # Step 2: Log in to your account
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    password_field.submit()
    time.sleep(5)

    # Step 3: Navigate to the event page
    driver.get("https://spond.com/your_event_url")  # Replace with your event URL
    time.sleep(3)

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
