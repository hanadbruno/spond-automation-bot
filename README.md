# Spond Automation Bot

## Overview
The **Spond Automation Bot** is a Python-based automation tool designed to help users interact with events on the Spond platform. This bot automatically logs into your Spond account, navigates to a specific event page, and accepts the event based on the specified schedule. It's designed to work seamlessly with Safari WebDriver, making it easy to automate event management for Spond users.

This project leverages **GitHub Actions** for scheduled automation and utilizes **Selenium WebDriver** for browser interaction. The bot runs securely with environment variables stored in GitHub Secrets, ensuring your credentials are safely managed.

---

## Features
- **Automatic Login**: Logs into your Spond account using your email and password stored as GitHub secrets.
- **Event Navigation**: Automatically navigates to your desired event page.
- **Event Acceptance**: Accepts events based on the scheduled time.
- **Schedule-based Automation**: Runs automatically on specified days (Wednesdays and Fridays) at set times, without any manual input.

---

## Requirements

To use this automation script, you'll need the following:

- **Python 3.9+**
- **GitHub repository secrets** for `EMAIL` and `PASSWORD`
- **Safari WebDriver** (installed and enabled in your system or via GitHub Actions)

---

## Setup

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/spond-automation.git
cd spond-automation

2. Install Dependencies
Install the required Python dependencies:
pip install -r requirements.txt
```

3. Set Up GitHub Secrets
In your GitHub repository, navigate to Settings > Secrets and add the following secrets:

EMAIL: Your Spond account email address
PASSWORD: Your Spond account password - 
These secrets will be used to securely log in to your Spond account during the automation process.

4. Set Up GitHub Actions
   
The workflow is already configured to run the bot automatically on Wednesdays at 17:00 UTC and Fridays at 15:00 UTC. You can modify the schedule in the .github/workflows/spond_automation.yml file if needed.

How It Works:

The bot uses Selenium WebDriver to interact with the Safari browser and automate the login process on the Spond platform.
Once logged in, the bot navigates to the group event page.
It waits until the specified time (Wednesday 17:00 or Friday 15:00) and then accepts the event automatically.
The workflow is managed using GitHub Actions, allowing the bot to run on a schedule without manual intervention.
Running the Bot
Once everything is set up and the GitHub Actions workflow is triggered (either manually or on the specified schedule), the bot will:

Login to Spond.
Navigate to the specified event page.
Wait for the scheduled time to accept the event.
Manual Run
To trigger the bot manually, simply go to the Actions tab in your GitHub repository and manually trigger the workflow.

Troubleshooting
Safari WebDriver Issues: Ensure that Safari WebDriver is properly enabled. If you encounter any issues running it in GitHub Actions, check the SafariDriver installation logs.
Incorrect Event Dates: Make sure that the event date format matches the expected format. If you run into issues parsing the event time, check the Spond page for updates in the event time format.

Contributions:

Contributions are welcome! If you find a bug or would like to suggest improvements, feel free to fork the repository and submit a pull request. We appreciate any help to make this project better!
