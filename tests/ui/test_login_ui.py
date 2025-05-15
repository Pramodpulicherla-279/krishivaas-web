import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def test_homepage_load(browser):
    browser.get("https://staging.krishivaas.ai/")
    assert "Krishivaas" in browser.title

def test_login(browser):
    browser.get("https://staging.krishivaas.ai/login")
    wait = WebDriverWait(browser, 10)
    username = wait.until(EC.presence_of_element_located((By.ID, "email")))
    password = wait.until(EC.presence_of_element_located((By.ID, "password")))
    submit = wait.until(EC.element_to_be_clickable((By.ID, "login")))

    username.send_keys("dmart@yopmail.com")
    password.send_keys("Dmart@!2024")
    submit.click()

    assert "Welcome" in browser.page_source