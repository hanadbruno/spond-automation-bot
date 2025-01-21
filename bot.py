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
            event_date_str = translate_norwegian_days(event_date_str)
            return datetime.strptime(event_date_str, "%A kl. %H:%M")
        except ValueError:
            raise ValueError(f"Date format not recognized: {event_date_str}")

# Function to get the next event's correct time based on the schedule
# Function to get the next event's correct time based on the schedule
def get_next_event_time():
    # Define the event times (in UTC)
    event_times = [
        {"day": 2, "hour": 16, "minute": 0},  # Wednesday at 17:00 CET (UTC 16:00)
        {"day": 5, "hour": 14, "minute": 0},  # Friday at 15:00 CET (UTC 14:00)
        {"day": 7, "hour": 14, "minute": 0},  # Sunday at 15:00 CET (UTC 14:00)
    ]

    # Get current time in UTC
    current_time = datetime.utcnow()

    # Loop through the event times and find the next scheduled event time
    for event_time in event_times:
        next_event_time = current_time.replace(hour=event_time["hour"], minute=event_time["minute"], second=0, microsecond=0)
        
        # Check if the event is later this week
        if current_time.weekday() < event_time["day"]:  # The event day is later this week
            days_until_event = (event_time["day"] - current_time.weekday()) % 7
            next_event_time = current_time + timedelta(days=days_until_event)
            return next_event_time.replace(hour=event_time["hour"], minute=event_time["minute"], second=0, microsecond=0)

        elif current_time.weekday() == event_time["day"] and next_event_time > current_time:  # Same day event but later time
            return next_event_time
        
    # If no upcoming events this week, schedule for next week's event
    next_event_time = next_event_time.replace(year=current_time.year + 1)  # Adjust to the following year if needed

    return next_event_time

# Function to wait until the next event time
def wait_until_event():
    next_event_time = get_next_event_time()
    current_time = datetime.utcnow()

    buffer_time = timedelta(minutes=3)
    next_event_time_with_buffer = next_event_time - buffer_time

    if next_event_time_with_buffer > current_time:
        wait_time = (next_event_time_with_buffer - current_time).total_seconds()
        print(f"Waiting for {wait_time} seconds until the next event (with 3-minute buffer).")
        time.sleep(wait_time)
    else:
        print("Event time has already passed. Exiting...")

# Function to perform login and event handling for a user
def handle_user(email, password):
    safari_options = Options()
    driver = webdriver.Safari(options=safari_options)
    print("SafariDriver is being used.")

    try:
        driver.get("https://spond.com/landing/login")
        print("Opened login page.")

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

        driver.get("https://spond.com/client/groups/4AC9EBBFC5284E0BBB0B38760D5F2AC1")
        print("Navigated to the group event page.")

        event_card = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='pageContentWrapper']/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]"))
        )

        event_url = event_card.get_attribute("href")
        if not event_url:
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

        wait_until_event()

        driver.get(event_url)
        retry_count = 0
        while True:
            try:
                accept_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@name='accept-button' and not(@disabled)]"))
                )
                accept_button.click()
                print("Successfully accepted the event!")
                break  # Stop when accepted
            except Exception:
                retry_count += 1
                print(f"Accept button not ready yet, retrying ({retry_count} attempts)...")
                time.sleep(10)  # Retry every 10 seconds
        

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Main logic to handle multiple users
users = [
    {"email": os.getenv("EMAIL"), "password": os.getenv("PASSWORD")},
    {"email": os.getenv("EMAIL1"), "password": os.getenv("PASSWORD1")}
]

for user in users:
    if user["email"] and user["password"]:
        print(f"Processing user: {user['email']}")
        handle_user(user["email"], user["password"])
    else:
        print("Missing credentials for one of the users.")
