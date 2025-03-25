import pytest
from selenium import webdriver
from utils.config import Config

@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    if Config.HEADLESS:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()