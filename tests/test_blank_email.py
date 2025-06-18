import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        'document.querySelectorAll("[aria-label=\'Privacy Preferences\'], .truste_overlay, .truste_popframe").forEach(e => e.remove());'
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
    driver.save_screenshot("no_email_landing_page.png")

    # Trigger continue without filling email
    try:
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

        # Intentionally don't type anything into email field
        logger.info("Leaving email field blank.")

        # Use JavaScript to try submitting the form and trigger the browser validation
        driver.execute_script("arguments[0].click();", continue_button)
        time.sleep(1)  # Wait for browser validation to appear
        driver.save_screenshot("empty_email_error.png")
        logger.info("Screenshot taken for empty email validation.")
    except TimeoutException:
        logger.error("Email step failed or element not found.")
        driver.save_screenshot("empty_email_timeout.png")

except WebDriverException as e:
    logger.error(f"Unexpected WebDriver error: {e}")
    driver.save_screenshot("unexpected_webdriver_error.png")

finally:
    driver.quit()
