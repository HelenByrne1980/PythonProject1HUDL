from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def get_wait(driver, timeout=15):
    return WebDriverWait(driver, timeout)
