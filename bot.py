import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to map Norwegian day names to English
def translate_norwegian_days(date_str):
    day_map = {
        "mandag": "Monday",
        "tirsdag": "Tuesday",
        "onsdag": "Wednesday",
        "torsdag": "Thursday",
        "fredag": "Friday",
        "lørdag": "Saturday",
        "søndag": "Sunday"
    }
    for no_day, en_day in day_map.items():
        if no_day in date_str:
            return date_str.replace(no_day, en_day)
    return date_str

# Function to parse event date
def parse_event_date(event_date_str):
    today = datetime.now()
    if "I dag" in event_date_str:
        time_str = event_date_str.split("kl. ")[1]
        event_time = datetime.strptime(time_str, "%H:%M")
        return today.replace(hour=event_time.hour, minute=event_time.minute, second=0, microsecond=0)
    elif "I morgen" in event_date_str:
        time_str = event_date_str.split("kl. ")[1]
        event_time = datetime.strptime(time_str, "%H:%M")
        return (today + timedelta(days=1)).replace(hour=event_time.hour, minute=event_time.minute, second=0, microsecond=0)
    else:
        try:
            # Translate Norwegian day names to English
            event_date_str = translate_norwegian_days(event_date_str)
            return datetime.strptime(event_date_str, "%A kl. %H:%M")
        except ValueError:
            raise ValueError(f"Date format not recognized: {event_date_str}")

# Initialize WebDriver for Safari
safari_options = Options()
driver = webdriver.Safari(options=safari_options)
print("SafariDriver is being used.")

try:
    # Step 1: Open the login page
    driver.get("https://spond.com/landing/login")
    print("Opened login page.")

    # Step 2: Login
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    print(f"Email: {email}")
    print(f"Password: {password}")
    if not email or not password:
        raise ValueError("Email or password is missing in the environment variables.")

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/root/app-login/div/div[2]/section[1]/div[2]/form/div[1]/input"))
    )
    email_field.send_keys(email)

    password_field = driver.find_element(By.XPATH, "/html/body/root/app-login/div/div[2]/section[1]/div[2]/form/div[2]/input")
    password_field.send_keys(password)

    login_button = driver.find_element(By.XPATH, "/html/body/root/app-login/div/div[2]/section[1]/div[2]/form/spinner-button/button/span")
    login_button.click()
    print("Login submitted.")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='spond-header-account-name']"))
    )
    print("Login successful!")

    # Step 3: Navigate to the group event page
    driver.get("https://spond.com/client/groups/4AC9EBBFC5284E0BBB0B38760D5F2AC1")
    print("Navigated to the group event page.")

    # Step 4: Extract event details
    event_card = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='pageContentWrapper']/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]"))
    )
    
    # Check if the event card contains the `href`
    event_url = event_card.get_attribute("href")
    if not event_url:
        # Look for a clickable child link within the event card
        link_element = event_card.find_element(By.TAG_NAME, "a")
        event_url = link_element.get_attribute("href")

    if not event_url:
        raise ValueError("Event URL could not be found.")
    
    print(f"Found event: {event_url}")

    event_date_str = driver.find_element(By.XPATH, "//*[@id='event_card_start_time']").text
    event_date = parse_event_date(event_date_str)
    print(f"Event date: {event_date}")

    target_time = event_date - timedelta(days=2)
    current_time = datetime.now()

    if current_time < target_time:
        wait_time = (target_time - current_time).total_seconds()
        print(f"Waiting for {wait_time} seconds until the target time.")
        time.sleep(wait_time)

    # Step 5: Accept the event
    driver.get(event_url)
    for _ in range(10):  # Retry loop
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@name='accept-button' and not(@disabled)]"))
            )
            accept_button.click()
            print("Successfully accepted the event!")
            break
        except Exception as e:
            print("Accept button not ready yet, retrying...")
            time.sleep(10)
    else:
        print("Could not find accept button after multiple retries.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()