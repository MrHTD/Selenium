from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up WebDriver
def setup_driver():
    options = Options()
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

# login function
def login(driver):
    try:
        # Locate and click the "Sign Up/Sign in" button
        login_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//p[text()='Sign Up/Sign in']"))
        )
        scroll_to_element(driver, login_button)

        try:
            login_button.click()
            print("Opened login form!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", login_button)

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
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][.//div[contains(text(), 'Login')]]"))
        )
        scroll_to_element(driver, login_button)

        try:
            login_button.click()
            print("Login successful!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", login_button)

        return True

    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Login failed: {e}")

    return False
    
# login function
def signup(driver):
    try:
        # Locate and click the "Sign Up/Sign in" button
        signup_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//p[text()='Sign Up/Sign in']"))
        )
        scroll_to_element(driver, signup_button)

        try:
            signup_button.click()
            print("Opened login form!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", signup_button)

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
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][.//div[contains(text(), 'Login')]]"))
        )
        scroll_to_element(driver, login_button)

        try:
            login_button.click()
            print("Login successful!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", login_button)

        return True

    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Login failed: {e}")

    return False

# Main Function
def main():
    driver = setup_driver()
    driver.get("https://mawrid.user.devxonic.com")
    
    try:    
    #     if login(driver):
    #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
    #         # Scroll to Swiper Section
    #         swiper_section = WebDriverWait(driver, 5).until(
    #             EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'relative w-full')]"))
    #         )
    #         scroll_to_element(driver, swiper_section)
            
    #         product(driver)

    #         # Uncomment this if you want to log out at the end
    #         # logout(driver)

    # except Exception as e:
    #     print(f"Error encountered: {e}")
        product(driver)
        
        product_test(driver)
    
    finally:
        time.sleep(3)
        driver.quit()
    
main()