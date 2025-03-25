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

<<<<<<< HEAD
# login function
def login(driver):
    try:
        # Wait for the email input field
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='identifier']"))
=======
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
>>>>>>> a6d6082157f2e285df71bad9f59e4d3c6b108aa5
        )
        scroll_to_element(driver, email_field)
        email_field.send_keys("james268@gmail.com")

        # Wait for the password input field
        password_field = WebDriverWait(driver, 10).until(
<<<<<<< HEAD
            EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
=======
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
>>>>>>> a6d6082157f2e285df71bad9f59e4d3c6b108aa5
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
<<<<<<< HEAD
    except Exception as e:
        print(f"Login failed: {e}")
=======
        raise TestFailedException(f"Login failed due to timeout: {e}")
    except Exception as e:
        print(f"Login failed: {e}")
        raise TestFailedException(f"Login failed: {e}")
    
def createstore(driver):
    try:
        
        # Wait for the shop_name input field
        shop_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'border rounded p-1')]"))
        )
        scroll_to_element(driver, shop_name)
        shop_name.click()
        print("Shop named!!")
        shop_name.clear()
        shop_name.send_keys("james shop")
        
        # Locate the file input
        cover_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "coverImageUpload"))
        )
        scroll_to_element(driver, cover_img)
        print("Image Uploaded!")
        cover_img.send_keys("/home/devxonic/Downloads/cover.jpg")
        
        # Locate the file input
        profile_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "profileImageUpload"))
        )
        print("Profile Image Uploaded!")
        profile_img.send_keys("/home/devxonic/Downloads/profile.jpg")
        
        
        # Locate and click the category input field
        category_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='select category']"))
        )
        category_input.click()
        print("Category Selected!")
        
        category_option = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[contains(@class, 'max-h-48')]/li/span"))
        )
        random.choice(category_option).click()
        
        
        
        # First dropdown selection
        day_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select an option' and contains(@class, 'w-full bg-transparent')])[1]"))
        )
        day_input.click()
        print("Day Selected!")

        day_option = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[contains(@class, 'max-h-48')]/li/span"))
        )
        random.choice(day_option).click()

        # Second dropdown selection
        day_input1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select an option' and contains(@class, 'w-full bg-transparent')])[2]"))
        )
        day_input1.click()
        
        day_option1 = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[contains(@class, 'max-h-48')]/li/span"))
        )
        random.choice(day_option1).click()
        
        
        
        for index in range(1, 3):  # Loop for first and second time inputs
            time_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"(//div[contains(@class, 'block px-2 py-3 border rounded-md focus:outline-none w-full cursor-pointer')])[{index}]"))
            )        
            scroll_to_element(driver, time_input)
            time_input.click()
            print("Time Selected!")

            # Set random hour (1-12)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and @min='1' and @max='12']"))
            ).send_keys(str(random.randint(1, 12)))

            # Set random minute (0-59)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and @min='0' and @max='59']"))
            ).send_keys(str(random.randint(0, 59)))

            # Toggle AM/PM randomly
            if random.choice([True, False]):
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'AM') or contains(text(), 'PM')]"))
                ).click()

            # Click Confirm
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
            ).click()
            
            
            
        shop_desc = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Store Description')]/following-sibling::input[@type='text']"))
        )
        scroll_to_element(driver, shop_desc)
        shop_desc.click()
        shop_desc.send_keys("shop_desc")
        print("Shop Description Added!")
        
        shop_addr = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='address' and contains(@class, 'block w-full px-2 py-2 border border-gray-300')]"))
        )
        scroll_to_element(driver, shop_addr)
        shop_addr.click()
        shop_addr.send_keys("shop_addr")
        print("Shop Address Added!")
        
        pickup_loc = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Pickup locations:')]/following-sibling::input[@type='text']"))
        )
        scroll_to_element(driver, pickup_loc)
        pickup_loc.click()
        pickup_loc.send_keys("pickup_loc")
        print("Pickup locations Added!")
        
        delivery_loc = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Default delivery locations:')]/following-sibling::input[@type='text']"))
        )
        scroll_to_element(driver, delivery_loc)
        delivery_loc.click()
        delivery_loc.send_keys("Delivery location")
        print("Delivery locations Added!")
        
        # Locate and click the Continue button
        Continue = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Continue')]"))
        )
        scroll_to_element(driver, Continue)

        try:
            Continue.click()
            print("Store Created successful!")
        except ElementNotInteractableException:
            print("Regular click failed, using JS click.")
            driver.execute_script("arguments[0].click();", Continue)
        
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in create store function: {e}")

    return False
        
>>>>>>> a6d6082157f2e285df71bad9f59e4d3c6b108aa5

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
<<<<<<< HEAD
                tab_name = tab.text.strip()

                if tab.is_displayed(): # Check if visible
                    try:
                        scroll_to_element(driver, tab)
                        ActionChains(driver).move_to_element(tab).pause(2).click().perform()
                        time.sleep(1)  # Slow down the clicks
                    except ElementClickInterceptedException:
                        driver.execute_script("arguments[0].click();", tab)  # Fallback JS click

                    print(f"Clicked on Tab {index + 1}: {tab_name}")
                else:
                    print(f"Tab {index + 1} ({tab_name}) is not visible, skipping.")
=======

                if tab.is_displayed():  # Check if visible
                    try:
                        ActionChains(driver).move_to_element(tab).click().perform()
                    except ElementClickInterceptedException:
                        driver.execute_script("arguments[0].click();", tab)  # Fallback JS click

                    print(f"Clicked on Tab {index + 1}")
                else:
                    print(f"Tab {index + 1} is not visible, skipping.")
>>>>>>> a6d6082157f2e285df71bad9f59e4d3c6b108aa5

            except StaleElementReferenceException:
                print(f"Tab {index + 1} became stale, skipping.")
            
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in sidebar function: {e}")
<<<<<<< HEAD
        
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
=======

    return False

>>>>>>> a6d6082157f2e285df71bad9f59e4d3c6b108aa5
    
# Main Function
def main():
    driver = setup_driver()
    driver.get("https://mawrid.vendor.devxonic.com")
    
    try:    
        login(driver)
        
<<<<<<< HEAD
        sidebar(driver)
        
        logout(driver)
=======
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        createstore(driver)
        
        # sidebar(driver)
        
        # Uncomment this if you want to log out at the end
        # logout(driver)
>>>>>>> a6d6082157f2e285df71bad9f59e4d3c6b108aa5

    except Exception as e:
        print(f"Error encountered: {e}")
    
    finally:
        time.sleep(3)
        driver.quit()
    
main()