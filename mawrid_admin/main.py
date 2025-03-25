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

# login function
def login(driver):
    try:
        # Wait for the email input field
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='identifier']"))
        )
        scroll_to_element(driver, email_field)
        email_field.send_keys("mawadmin@gmail.com")

        # Wait for the password input field
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        scroll_to_element(driver, password_field)
        password_field.send_keys("000012345")

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
    except Exception as e:
        print(f"Login failed: {e}")
        
# Check if the page is loaded properly after clicking a tab
def check_page_status(driver):
    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "404" in body_text or "Page Not Found" in body_text:
            print("404 Error: Page Not Found!")
            return False
        if not body_text.strip():
            print("Error: The page loaded but is empty!")
            return False
        return True
    except Exception as e:
        print(f"Error while checking page status: {e}")
        return False

#sidebar Function
def sidebar(driver):
    try:
        tabs = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'flex items-center cursor-pointer')]//span[contains(@class, 'flex py-3 px-3 items-center w-full h-full')]"))
        )
    
        for index in range(len(tabs)):  # Avoid iterating stale elements
            try:
                # Re-locate the elements to prevent StaleElementReferenceException
                tabs = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'flex items-center cursor-pointer')]//span[contains(@class, 'flex py-3 px-3 items-center w-full h-full')]"))
                )
                tab = tabs[index]
                tab_name = tab.text.strip()

                if tab.is_displayed(): # Check if visible
                    try:
                        scroll_to_element(driver, tab)
                        ActionChains(driver).move_to_element(tab).pause(2).click().perform()
                        time.sleep(1)  # Slow down the clicks
                        
                        # Check if page loaded properly after clicking
                        if not check_page_status(driver):
                            print(f"Error: {tab_name} tab did not load correctly!")
                            continue  # Skip to the next tab
                        
                        print(f"Clicked on Tab {index + 1}: {tab_name}")
                        
                    except ElementClickInterceptedException:
                        driver.execute_script("arguments[0].click();", tab)  # Fallback JS click

                else:
                    print(f"Tab {index + 1} ({tab_name}) is not visible, skipping.")

            except StaleElementReferenceException:
                print(f"Tab {index + 1} became stale, skipping.")
            
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in sidebar function: {e}")
        
# Logout Funtion
def logout(driver):
    try:
        # Wait for and find "Login as:" button
        logout = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex items-center')]"))
        )
        scroll_to_element(driver, logout)

        try:
            logout.click()
            print("Logout Success!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", logout)
    
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Logout failed: {e}")
    
# Main Function
def main():
    driver = setup_driver()
    driver.get("https://mawrid.admin.devxonic.com")
    
    try:    
        login(driver)
        
        sidebar(driver)
        
        # logout(driver)

    except Exception as e:
        print(f"Error encountered: {e}")
    
    finally:
        time.sleep(3)
        driver.quit()
    
main()