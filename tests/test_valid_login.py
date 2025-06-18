import os
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from dotenv import load_dotenv
from utils.driver_setup import get_driver, get_wait

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv("HUDL_EMAIL")
PASSWORD = os.getenv("HUDL_PASSWORD")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Email loaded: {EMAIL}")
logger.info(f"Password loaded: {'*' * len(PASSWORD) if PASSWORD else None}")

# Setup driver and wait
driver = get_driver()
wait = get_wait(driver)

try:
    driver.get("https://www.hudl.com")
    time.sleep(2)

    # Handle cookie banner
    try:
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        driver.execute_script("arguments[0].click();", cookie_button)
        logger.info("Cookie banner dismissed.")
    except Exception:
        logger.info("No cookie banner found or failed to dismiss it.")

    # Remove privacy overlays
    driver.execute_script(
        'document.querySelectorAll("[aria-label=\\\"Privacy Preferences\\\"], .truste_overlay, .truste_popframe").forEach(e => e.remove());')

    # Open login dropdown
    try:
        login_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa-id='login-select']")))
        driver.execute_script("arguments[0].click();", login_dropdown)
        logger.info("Login dropdown opened.")
    except Exception as e:
        logger.error(f"Dropdown toggle not found: {e}")

    # Click Hudl login option
    try:
        hudl_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa-id='login-hudl']")))
        driver.execute_script("arguments[0].click();", hudl_login)
        logger.info("Clicked Hudl login.")
    except Exception as e:
        logger.error(f"Failed to click Hudl login: {e}")

    # Wait for redirect
    time.sleep(3)
    current_url = driver.current_url
    logger.info(f"Redirected to login page: {current_url}")

    # Screenshot after redirect
    driver.save_screenshot("debug_login_page.png")

    try:
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(EMAIL)
        logger.info("Entered email.")

        continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", continue_button)
        logger.info("Clicked Continue button.")

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(PASSWORD)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", login_button)
        logger.info("Clicked login button.")

        # Wait for successful login by checking user dashboard
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "header, nav, .hui-globalheader")))
        logger.info("Login successful!")

        # Screenshot after login
        driver.save_screenshot("login_success.png")
    except TimeoutException:
        logger.error("Login form elements not found or login failed.")
        driver.save_screenshot("login_failed.png")

except WebDriverException as e:
    logger.error(f"Unexpected WebDriver error: {e}")

finally:
    driver.quit()








