from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time, os

url = os.getenv("STREAMLIT_APP_URL")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(url)
time.sleep(10)

try:
    button = driver.find_element(By.XPATH, "//button[contains(., 'Yes, get this app back up!')]")
    button.click()
    print("✅ App woke up successfully!")
except Exception:
    print("ℹ️ App already awake or no wake-up button found.")

driver.quit()
