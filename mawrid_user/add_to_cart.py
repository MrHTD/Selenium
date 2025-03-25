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

        # Add verification
        if not verify_login_success(driver):
            raise TestFailedException("Login verification failed")
        print("Login successful!")
        return True

    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
        raise TestFailedException(f"Login failed due to timeout: {e}")
    except Exception as e:
        print(f"Login failed: {e}")
        raise TestFailedException(f"Login failed: {e}")

# Function to click Product
def product(driver):
    try:
        swiper_section = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'relative w-full')]//div[contains(@class, 'swiper swiper-initialized')]"))
        )
        scroll_to_element(driver, swiper_section)

        # add_product_to_cart(driver, 3)  # Add 3 product
        add_products = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'bg-primary text-white border-primary')]"))
        )   

        for index, add_product in enumerate(add_products):
            if index == 3:
                break
            ActionChains(driver).move_to_element(add_product).click().perform()
            print(f"Product Added to Cart {index}")
            
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in product function: {e}")

    return False

#Cart Function
def Cart(driver):
    try:
        scroll = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'inline-flex justify-end items-center space-x-5 flex-1')]"))
        )
        scroll_to_element(driver, scroll)
        
        cart = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//p//span[text()='Cart']"))
        )
        scroll_to_element(driver, cart)
            
        try:
            print(f"Clicked to cart btn")
            cart.click()
        except Exception as e:
            print(f"Error navigating swiper: {e}")
            
        checkout = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][.//div[contains(text(), 'Proceed to checkout')]]"))
        )
        scroll_to_element(driver, checkout)
            
        try:
            print(f"Clicked to checkout btn")
            checkout.click()
        except Exception as e:
            print(f"Error navigating swiper: {e}")
            
        
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in product function: {e}")

#Checkout Function
def Checkout(driver):
    try:
        # Wait for the email input field
        first_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='First name']"))
        )
        scroll_to_element(driver, first_name)
        first_name.clear()
        first_name.send_keys("Yummy")
        print(f"first name entered: {first_name.get_attribute('value')}")
        
        last_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Last name']"))
        )
        scroll_to_element(driver, last_name)
        last_name.clear()
        last_name.send_keys("123")
        print(f"last name entered: {last_name.get_attribute('value')}")
        
        address = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='address']"))
        )
        scroll_to_element(driver, address)
        address.clear()
        address.send_keys("abcd street")
        print(f"address entered: {address.get_attribute('value')}")
        
        appar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='apartment']"))
        )
        scroll_to_element(driver, appar)
        appar.clear()
        appar.send_keys("3rd floor")
        print(f"apartment entered: {appar.get_attribute('value')}")
        
        city = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='city']"))
        )
        scroll_to_element(driver, city)
        city.clear()
        city.send_keys("abcd street")
        print(f"city entered: {city.get_attribute('value')}")
        
        region = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select Region' and contains(@class, 'w-full bg-transparent focus:outline-none')])"))
        )
        region.click()
        print("Region Selected!")
        region_option = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[contains(@class, 'max-h-48')]/li/span"))
        )
        random.choice(region_option).click()
        
        state = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select State' and contains(@class, 'w-full bg-transparent focus:outline-none')])"))
        )
        state.click()
        print("State Selected!")
        state_option = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[contains(@class, 'max-h-48')]/li/span"))
        )
        random.choice(state_option).click()
        
        zip = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='zip']"))
        )
        scroll_to_element(driver, zip)
        zip.clear()
        zip.send_keys("111111")
        print(f"zip entered: {zip.get_attribute('value')}")
        
        phone = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='phone']"))
        )
        scroll_to_element(driver, phone)
        phone.clear()
        phone.send_keys("12345678910")
        print(f"phone entered: {phone.get_attribute('value')}")
        
                    
        checkout_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][.//div[contains(text(), 'Continue to shipping')]]"))
        )
        scroll_to_element(driver, checkout_btn)
            
        try:
            print(f"Checkout Succesfull!")
            checkout_btn.click()
        except Exception as e:
            print(f"Error navigating swiper: {e}")
        
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in product function: {e}")

# Main Function
def main():
    driver = setup_driver()
    driver.get("https://mawrid.user.devxonic.com")
    
    try:    
        login(driver)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        product(driver)
    
        Cart(driver)
        
        Checkout(driver)
        
    except Exception as e:
        print(f"Error encountered: {e}")
    
    finally:
        time.sleep(3)
        driver.quit()
    
main()