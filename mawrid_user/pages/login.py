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
        # Find all product cards
        cards = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'swiper-slide')]//div[contains(@class, 'grid')]//div[contains(@class, 'overflow-hidden row-span-1')]//div[contains(@class, 'p-2 flex')]"
        )
        
        if not cards:
            print("No cards found.")
            return False

        # Click the first product
        card = cards[0]
        try:
            product = card.find_element(By.XPATH, "//div[contains(@class, 'grid grid-rows-2 flex-flex-shrink-0 ')]")
            scroll_to_element(driver, product)

            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(product))

            try:
                product.click()
                print("Product clicked successfully!")
                return True
            except ElementNotInteractableException:
                print("Regular click failed, using JavaScript click.")
                driver.execute_script("arguments[0].click();", product)

        except NoSuchElementException:
            print("Product not found.")
            return False
            
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in product function: {e}")

    return False

#
def product_test(driver):
    count = 0
    try:
        scroll = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex flex-col md:flex-row gap-4')]"))
        )
        scroll_to_element(driver, scroll)
        
        # Number of times to click
        num_clicks = 2
        
        for _ in range(num_clicks):
            plus_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'w-8 h-8 flex items-center justify-center')]"))
            )
            count += 1 
            try:
                print(f"Product add {count}")
                plus_button.click()
            except Exception as e:
                print(f"Error navigating swiper: {e}")
                break
        
        for _ in range(num_clicks):
            minus_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'w-8 h-8 flex items-center text-center')]"))
            )
            count -= 1 
            try:
                print(f"Product remove {count}")
                minus_button.click()
            except Exception as e:
                print(f"Error navigating swiper: {e}")
                break
            
        # add_to_cart = WebDriverWait(driver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[contains(@type, 'submit') and contains(@class, 'font-medium')]"))
        # )
        # try:
        #     print(f"Clicked add to cart")
        #     add_to_cart.click()
        # except Exception as e:
        #     print(f"Error navigating swiper: {e}")
    
            
        # scroll_1 = WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'relative w-[100%]')]//div[contains(@class, 'flex items-center gap-5 overflow-x-auto')]"))
        # )
        # scroll_to_element(driver, scroll_1)
                    
        # Find all clickable images
        images = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'p-1 rounded-md')]"))
        )   

        # Click each image
        for index, image in enumerate(images):
            ActionChains(driver).move_to_element(image).click().perform()
            print(f"Clicked on Image {index + 1}")
            
        for index, image in enumerate(reversed(images)):
            ActionChains(driver).move_to_element(image).click().perform()
            print(f"Clicked on Image {len(images) - index}")
        
        ################################################        
        scroll_2 = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'w-full flex flex-row sm:border-b border-gray-300')]"))
        )
        scroll_to_element(driver, scroll_2)
        
        tabs = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'p-4 text-center')]"))
        )   

        # Click each tabs
        for index, tab in enumerate(tabs):
            ActionChains(driver).move_to_element(tab).click().perform()
            print(f"Clicked on Tab {index + 1}")
        
        for index, tab in enumerate(reversed(tabs)):
            ActionChains(driver).move_to_element(tab).click().perform()
            print(f"Clicked on Tab {len(tabs) - index}")    
            
        
    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in product function: {e}")

    return False

#Review function
def review(driver):
    try:
        #review btn
        review = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][.//div[contains(text(), 'Write a review')]]"))
        )
        try:
            print(f"Clicked on review button")
            review.click()
        except Exception as e:
            print(f"Error navigating swiper: {e}") 
            
        # Find all star rating buttons
        stars = driver.find_elements(By.CSS_SELECTOR, ".flex.space-x-1.mt-2 button")
        random_star = random.choice(stars)
        ActionChains(driver).move_to_element(random_star).click().perform()
        print(f"Clicked on Star {stars.index(random_star) + 1}")
        
        # List of random reviews
        random_reviews = [
            "Great product! Really satisfied with the quality.",
            "Not bad, but could be improved in some areas.",
            "Absolutely love it! Highly recommend to everyone.",
            "Decent, but I expected better based on the description.",
            "Terrible experience. Won't buy again!"
        ]
        
        review = driver.find_element(By.CSS_SELECTOR, "textarea.w-full.border") 
        random_review = random.choice(random_reviews)
        # Enter the random review
        review.clear()
        review.send_keys(random_review)
        print(f"Entered review: {random_review}")
        
        # img_url = "https://upload.devxonic.com/file/1000200062.jpg"
        # upload_div = driver.find_element(By.CSS_SELECTOR, "div.border.border-dashed")
        # upload_div.click()
        # time.sleep(1)
        # print(f"Uploaded image: {img_url}")
        
        #review submit btn
        review_submit = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][.//div[contains(text(), 'Submit')]]"))
        )
        try:
            review_submit.click()
            print(f"Review Submitted!")
        except Exception as e:
            print(f"Error navigating swiper: {e}")         
        

    except TimeoutException as e:
        print(f"Timeout: Element not found - {e}")
    except Exception as e:
        print(f"Error in product function: {e}")

    return False
    

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
    driver.get("https://mawrid.user.devxonic.com")
    
    try:    
        login(driver)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        product(driver)
    
        product_test(driver)
        
        # review(driver)
        
        # Uncomment this if you want to log out at the end
        # logout(driver)

    except Exception as e:
        print(f"Error encountered: {e}")
    
    finally:
        time.sleep(3)
        driver.quit()
    
main()