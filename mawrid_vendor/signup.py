from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from faker import Faker
import random

fake = Faker()

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
        random_name = fake.first_name()
        random_email = f"{random_name.lower()}{random.randint(100,999)}@gmail.com"
        random_phone = str(random.randint(10000000000, 99999999999))  # 11-digit phone number
            
        # Locate and click the "Sign Up/Sign in" button
        signup_button = WebDriverWait(driver, 5).until(
            # EC.presence_of_element_located((By.XPATH, "//p[text()='Sign Up']"))
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Signup')]"))
        )
        scroll_to_element(driver, signup_button)

        try:
            signup_button.click()
            print("Opened signup form!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", signup_button)
            
        # Wait for the email input field
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        scroll_to_element(driver, name_field)
        print(f"Name Entered: {random_name}")
        name_field.send_keys(random_name)
        
        # Wait for the email input field
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @type='identifier']"))
        )
        scroll_to_element(driver, email_field)
        print(f"Email Entered: {random_email}")
        email_field.send_keys(random_email)

        # Wait for the email input field
        phone_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@inputmode='numeric']"))
        )
        scroll_to_element(driver, phone_field)
        phone_field.send_keys(random_phone)
        print(f"Phone Entered: {random_phone}")

        # Wait for all password fields
        password_fields = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='password']"))
        )

        # Ensure at least two password fields exist
        if len(password_fields) >= 2:
            password_field, confirmpass_field = password_fields[:2]
            
            password = "123456"
            
            scroll_to_element(driver, password_field)
            password_field.send_keys(password)

            scroll_to_element(driver, confirmpass_field)
            confirmpass_field.send_keys(password)

            print(f"Password {password} and Confirm Password entered successfully!")
        else:
            print("Error: Could not find both password fields!")


        # Locate and click the login button
        signup = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Create')]"))
        )
        scroll_to_element(driver, signup)

        try:
            signup.click()
            print("Signup successful!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", signup)
        
        # Add verification
        if not verify_login_success(driver):
            raise TestFailedException("Login verification failed")
        print("Login successful!")
        return True

    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
        raise TestFailedException(f"Signup failed due to timeout: {e}")
    except Exception as e:
        print(f"Signup failed: {e}")
        raise TestFailedException(f"Signup failed: {e}")


# Logout Funtion
def logout(driver):
    try:
        # Wait for and find "Login as:" button
        login_as_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'inline-flex')]//p[text()='Login as:']"))
        )
        scroll_to_element(driver, login_as_button)

        try:
            login_as_button.click()
            print("Opened logout menu!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", login_as_button)

        # Wait for and find "Logout" button
        logout_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'block bg-white fixed')]//p[text()='Logout']"))
        )
        scroll_to_element(driver, logout_button)

        try:
            logout_button.click()
            print("Logout successful!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", logout_button)

        return True
    
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Login failed: {e}")

    return False


# Main Function
def main():
    driver = setup_driver()
    driver.get("https://mawrid.vendor.devxonic.com")
    
    try:    
        login(driver)
        
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        
        # Uncomment this if you want to log out at the end
        # logout(driver)

    except Exception as e:
        print(f"Error encountered: {e}")
    
    finally:
        time.sleep(3)
        driver.quit()
    
main()