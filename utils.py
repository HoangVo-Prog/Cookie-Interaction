import logging
import random
import tempfile
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


CHROME_DRIVER_VERSION = 133
HEADLESS = True


def setup_driver():
    """
    Initializes a Chrome WebDriver instance with undetected-chromedriver.
    """
    chrome_options = uc.ChromeOptions()

    # Use a unique temporary directory for each worker to avoid conflicts
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument(f"--data-path={temp_dir}")

    # General browser settings
    chrome_options.add_argument("--window-size=1920x1080")  # Set the window size explicitly for headless
    chrome_options.add_argument("--disable-gpu")  # Disable GPU to avoid rendering issues in headless mode
    chrome_options.add_argument("--disable-infobars")  # Prevents the "Chrome is being controlled by automated test software" infobar
    chrome_options.add_argument("--disable-extensions")  # Disable extensions to speed up the process
    chrome_options.add_argument("--disable-browser-side-navigation")  # Disable some side navigations
    chrome_options.add_argument("--disable-site-isolation-trials")  # To avoid some potential rendering issues
    chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (useful in headless environments)
    # Headless Mode (Avoid Detection)
    chrome_options.headless = HEADLESS

    # Prevent detection by removing automation flags and using a random User-Agent
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation detection

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QQ1A.200205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.120 Mobile Safari/537.36",
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    chrome_options.add_argument("--user-data-dir=C:/Users/{userName}/AppData/Local/Google/Chrome/User Data/Profile {#}/")
    # Configure the WebDriver version if necessary
    if CHROME_DRIVER_VERSION:
        chrome_options.add_argument(f"--webdriver-version={CHROME_DRIVER_VERSION}")

    # Initialize the driver with subprocess to avoid blocking (useful in headless environments)
    try:
        driver = uc.Chrome(
            options=chrome_options,
            use_subprocess=True,
        )
        driver.maximize_window()  # Ensures window is maximized, even in headless mode
        logging.info("WebDriver initialized successfully.")

        return driver
    except Exception as e:
        logging.error(f"Failed to initialize WebDriver: {e}")
        raise


def perform_login(driver, email, password):
    """
    Automates the login process using the provided email and password.
    """
    try:
        print("Attempting login for email: %s", email)

        # Wait for the email input field to be visible and interactable
        email_field = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "identifierId"))
        )

        email_field.send_keys(email)

        driver.save_screenshot("before_email.png")
        logging.info("Save screenshot")
        next_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='identifierNext']"))
        )
        next_button.click()
        time.sleep(random.uniform(0.1, 0.6))  # Random delay
        time.sleep(10)

        # Optionally, take a screenshot to inspect the current page state
        driver.save_screenshot("email.png")
        logging.info("Save screenshot")

        # Wait for the password input field to be visible and interactable
        password_field = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(random.uniform(1, 2))  # Random delay
        time.sleep(5)  # Longer wait after login to ensure successful login
        logging.info("Login successful for email: %s", email)
        return 1
    except Exception as e:
        logging.error(f"Login failed for email: {email} - {e}")
        return None

