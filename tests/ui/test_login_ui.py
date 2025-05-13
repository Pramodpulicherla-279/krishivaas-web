import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def test_homepage_load(browser):
    browser.get("https://staging.krishivaas.ai/")
    assert "Example" in browser.title

def test_login(browser):
    browser.get("https://staging.krishivaas.ai/login")
    username = browser.find_element(By.ID, "email")
    password = browser.find_element(By.ID, "password")
    submit = browser.find_element(By.ID, "submit")
    
    username.send_keys("dmart@yopmail.com")
    password.send_keys("Dmart@!2024")
    submit.click()
    
    assert "Welcome" in browser.page_source