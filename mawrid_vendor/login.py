from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException,StaleElementReferenceException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# Set up WebDriver
def setup_driver():
    options = Options()
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Scroll to an element
def scroll_to_element(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(0.5)  # Allow animation

class TestFailedException(Exception):
    """Custom exception for test failures"""
    pass

def verify_login_success(driver):
    try:
        # Wait for an element that appears only after successful login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(., 'Login as:')]"))
        )
        print("Login verification: Success - User menu found")
        return True
    except TimeoutException:
        # If the element is not found, raise a custom exception with a descriptive message
        raise TestFailedException("Login verification failed - User menu not found")

# login function
def login(driver):
    try:

        # Wait for the email input field
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @type='identifier']"))
        )
        scroll_to_element(driver, email_field)
        email_field.send_keys("hammad@gmail.com")

        # Wait for the password input field
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        scroll_to_element(driver, password_field)
        password_field.send_keys("123456")

        # Locate and click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Login')]"))
        )
        scroll_to_element(driver, login_button)

        try:
            login_button.click()
            print("Login successful!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", login_button)
            
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
        raise TestFailedException(f"Login failed due to timeout: {e}")
    except Exception as e:
        print(f"Login failed: {e}")
        raise TestFailedException(f"Login failed: {e}")

#sidebar Function
def sidebar(driver):
    try:
        tabs = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'flex flex-row gap-3 items-center')]//span[contains(@class, 'flex py-3 px-3 items-center w-full h-full')]"))
        )
    
        for index in range(len(tabs)):  # Avoid iterating stale elements
            try:
                # Re-locate the elements to prevent StaleElementReferenceException
                tabs = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'flex flex-row gap-3 items-center')]//span[contains(@class, 'flex py-3 px-3 items-center w-full h-full')]"))
                )
                tab = tabs[index]

                if tab.is_displayed():  # Check if visible
                    try:
                        ActionChains(driver).move_to_element(tab).click().perform()
                    except ElementClickInterceptedException:
                        driver.execute_script("arguments[0].click();", tab)  # Fallback JS click

                    print(f"Clicked on Tab {index + 1}")
                else:
                    print(f"Tab {index + 1} is not visible, skipping.")

            except StaleElementReferenceException:
                print(f"Tab {index + 1} became stale, skipping.")
            
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in sidebar function: {e}")

    return False

    
# Main Function
def main():
    driver = setup_driver()
    driver.get("https://mawrid.vendor.devxonic.com")
    
    try:    
        login(driver)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        sidebar(driver)
        
        # Uncomment this if you want to log out at the end
        # logout(driver)

    except Exception as e:
        print(f"Error encountered: {e}")
    
    finally:
        time.sleep(3)
        driver.quit()
    
main()