import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EMAIL = "invalidemail.com"  # Invalid format (missing '@')
PASSWORD = os.getenv("HUDL_PASSWORD")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Using intentionally invalid email: {EMAIL}")
logger.info(f"Password loaded: {'*' * len(PASSWORD) if PASSWORD else None}")

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

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
        'document.querySelectorAll("[aria-label=\\"Privacy Preferences\\"], .truste_overlay, .truste_popframe").forEach(e => e.remove());')

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
    driver.save_screenshot("debug_invalid_email_redirect.png")

    try:
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(EMAIL)
        logger.info("Entered invalid email.")

        continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", continue_button)
        logger.info("Clicked Continue button.")

        time.sleep(2)
        try:
            error_box = wait.until(EC.visibility_of_element_located((By.ID, "error-element-username")))
            driver.execute_script("arguments[0].style.border='3px solid red'", error_box)
            screenshot_path = "invalid_email_error.png"
            driver.save_screenshot(screenshot_path)
            logger.info(f"Captured screenshot of invalid email error message: {screenshot_path}")
        except TimeoutException:
            fallback_path = "invalid_email_error_not_found.png"
            driver.save_screenshot(fallback_path)
            logger.warning("No error message found after submitting invalid email.")
            logger.info(f"Saved fallback debug screenshot: {fallback_path}")

    except TimeoutException:
        logger.error("Email step failed or interaction timed out.")
        driver.save_screenshot("invalid_email_timeout.png")

except WebDriverException as e:
    logger.error(f"Unexpected WebDriver error: {e}")

finally:
    driver.quit()
