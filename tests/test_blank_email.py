import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from utils.driver_setup import get_driver, get_wait

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get driver and wait objects
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
    driver.save_screenshot("screenshots/no_email_landing_page.png")

    # Try to submit without email
    email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

    logger.info("Leaving email field blank.")
    driver.execute_script("arguments[0].click();", continue_button)
    time.sleep(1)  # Allow browser to trigger validation

    driver.save_screenshot("screenshots/empty_email_error.png")
    logger.info("Captured screenshot of browser's email required field error.")

except TimeoutException:
    logger.error("Email step failed or element not found.")
    driver.save_screenshot("screenshots/empty_email_timeout.png")

except WebDriverException as e:
    logger.error(f"Unexpected WebDriver error: {e}")
    driver.save_screenshot("screenshots/unexpected_webdriver_error.png")

finally:
    driver.quit()

