import os
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from dotenv import load_dotenv
from utils.driver_setup import get_driver, get_wait

# Load environment variables
load_dotenv()
EMAIL = os.getenv("HUDL_EMAIL")
INVALID_PASSWORD = "WrongPassword123"

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Email loaded: {EMAIL}")
logger.info("Using intentionally incorrect password.")

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

    # Remove overlays
    driver.execute_script(
        'document.querySelectorAll("[aria-label=\'Privacy Preferences\'], .truste_overlay, .truste_popframe").forEach(e => e.remove());'
    )

    # Open login dropdown
    login_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa-id='login-select']")))
    driver.execute_script("arguments[0].click();", login_dropdown)
    logger.info("Login dropdown opened.")

    # Click Hudl login option
    hudl_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa-id='login-hudl']")))
    driver.execute_script("arguments[0].click();", hudl_login)
    logger.info("Clicked Hudl login.")

    time.sleep(3)
    driver.save_screenshot("screenshots/debug_invalid_login_redirect.png")

    # Fill in valid email
    email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    email_field.send_keys(EMAIL)
    logger.info("Entered email.")

    continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    driver.execute_script("arguments[0].click();", continue_button)
    logger.info("Clicked Continue button.")

    # Fill in invalid password
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(INVALID_PASSWORD)

    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    driver.execute_script("arguments[0].click();", login_button)
    logger.info("Clicked login button with incorrect password.")

    # Check for error message
    time.sleep(2)
    try:
        error_box = wait.until(EC.visibility_of_element_located((By.ID, "error-element-password")))
        driver.execute_script("arguments[0].style.border='3px solid red'", error_box)
        screenshot_path = "screenshots/invalid_login_error_message.png"
        driver.save_screenshot(screenshot_path)
        logger.info(f"Captured screenshot of error message: {screenshot_path}")
    except TimeoutException:
        fallback_path = "screenshots/invalid_login_no_error.png"
        driver.save_screenshot(fallback_path)
        logger.warning("No error message appeared.")
        logger.info(f"Saved fallback screenshot: {fallback_path}")

except WebDriverException as e:
    logger.error(f"Unexpected WebDriver error: {e}")

finally:
    driver.quit()


