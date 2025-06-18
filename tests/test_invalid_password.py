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

EMAIL = os.getenv("HUDL_EMAIL")
INVALID_PASSWORD = "WrongPassword123"  # Deliberately incorrect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Email loaded: {EMAIL}")
logger.info("Using intentionally incorrect password.")

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
        'document.querySelectorAll("[aria-label=\\"Privacy Preferences\\"], .truste_overlay, .truste_popframe").forEach(e => e.remove());'
    )

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
    driver.save_screenshot("debug_invalid_login_redirect.png")

    # Login attempt
    try:
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(EMAIL)
        logger.info("Entered email.")

        continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", continue_button)
        logger.info("Clicked Continue button.")

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(INVALID_PASSWORD)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", login_button)
        logger.info("Clicked login button with incorrect password.")

        # Wait and detect invalid login error message
        time.sleep(3)

        try:
            error_box = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "error-element-password"))
            )
            driver.execute_script("arguments[0].style.border='3px solid red'", error_box)
            screenshot_path = "invalid_login_error_message.png"
            driver.save_screenshot(screenshot_path)
            logger.info(f"Captured screenshot of invalid login error message: {screenshot_path}")
        except TimeoutException:
            fallback_path = "login_error_not_found_debug.png"
            driver.save_screenshot(fallback_path)
            logger.warning("No error message found after failed login attempt.")
            logger.info(f"Saved fallback debug screenshot: {fallback_path}")

    except TimeoutException:
        logger.error("Login form elements not found or interaction failed.")
        driver.save_screenshot("invalid_login_timeout.png")

except WebDriverException as e:
    logger.error(f"Unexpected WebDriver error: {e}")

finally:
    driver.quit()

