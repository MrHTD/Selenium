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

# Swiper navigation function
def navigate_swiper(driver, button_xpath, direction="next"):
    slide_index = 1
    while True:
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )

            if button.get_attribute("aria-disabled") == "true":
                print(f"Reached the last slide in {direction} direction at slide {slide_index}.")
                break

            print(f"{direction.capitalize()} button enabled. Clicking slide {slide_index}...")
            
            scroll_to_element(driver, button)

            try:
                button.click()
            except ElementNotInteractableException:
                print("Regular click failed. Using JavaScript click...")
                driver.execute_script("arguments[0].click();", button)

            slide_index += 1 if direction == "next" else -1
            time.sleep(0.1)

        except TimeoutException:
            print(f"{direction.capitalize()} button no longer visible. Stopping navigation.")
            break
        except Exception as e:
            print(f"Error during {direction} navigation: {e}")
            break

    print(f"Swiper navigation in {direction} direction completed successfully!")

# Function to click scan button
def click_scan_button(driver):
    try:
        cards = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'swiper-slide')]//div[contains(@class, 'grid')]//div[contains(@class, 'overflow-hidden row-span-1')]//div[contains(@class, 'p-2 flex')]"
        )
        if not cards:
            print("No cards found.")
            return False

        card = cards[0]
        scan_button = card.find_element(By.XPATH, ".//div[contains(@class, 'cursor-pointer')]")
        scroll_to_element(driver, scan_button)

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(scan_button))

        try:
            scan_button.click()
            print("Scan button click successful!")
            return True
        except ElementNotInteractableException:
            print("Regular click failed.")
            return False
    except NoSuchElementException:
        print("Scan button not found.")
        return False

# Function to navigate image slider
def image_slider(driver, button_xpath, steps=1, direction="right"):
    for _ in range(steps):
        try:
            button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )
            print(f"{direction.capitalize()} button found. Clicking...")

            try:
                button.click()
            except Exception as e:
                print(f"Error navigating swiper: {e}")
                break
        except TimeoutException:
            print(f"{direction.capitalize()} button no longer found.")
            break

# Function to close image slider
def close_slider(driver):
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'absolute top-4')]"))
        )
        print("Close button found!")

        try:
            close_button.click()
            print("Slider closed successfully.")
        except Exception:
            print("Close button click failed.")
    except TimeoutException:
        print("Close button not found in time.")

# Function to click all category sections
def click_categories(driver):
    try:
        category_section = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'grid')]"))
        )
        scroll_to_element(driver, category_section)

        clickable_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer mb-2 flex align-middle items-center justify-center')]")
        print(f"Total categories found: {len(clickable_divs)}")

        for index, div in enumerate(clickable_divs, start=1):
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", div)
                div.click()
                time.sleep(1)

                try:
                    text_element = div.find_element(By.XPATH, ".//following-sibling::div//p")
                    category_name = text_element.text.strip()
                except:
                    category_name = f"Category {index}"

                try:
                    # products = div.find_elements(By.XPATH, "//div[contains(@class, 'grid grid-rows-2')]")
                    products = div.find_elements(By.XPATH, "//div[contains(@class, 'grid grid-rows-2 flex-flex-shrink-0 rounded-2xl bg-white border border-gray-300 shadow-sm overflow-x-hidden hover:border-textsecondary max-w-[320px]')]")
                    num_products = len(products)
                except:
                    num_products = 0

                print(f"{category_name}: {num_products} products")

            except NoSuchElementException:
                print(f"Error clicking category {index}.")

        print("\nCategory clicking completed!")

    except TimeoutException:
        print("Categories section not found.")

# Main function
def main():
    driver = setup_driver()
    driver.get("https://mawrid.user.devxonic.com")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Step 1: Swiper navigation
        swiper_section = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'relative w-full')]"))
        )
        scroll_to_element(driver, swiper_section)
        navigate_swiper(driver, "//button[contains(@class, 'custom-swiper-next')]", direction="next")
        navigate_swiper(driver, "//button[contains(@class, 'custom-swiper-prev')]", direction="prev")

        # Step 2: Click scan button
        if click_scan_button(driver):
            time.sleep(0.5)

            # Step 3: Image slider navigation
            images = driver.find_elements(By.XPATH, "//img[contains(@class, 'rounded-md object-contain w-full')]")
            num_images = len(images)
            print(f"Total images found: {num_images}")

            image_slider(driver, "//button[contains(@class, 'absolute right-2')]", steps=num_images, direction="right")
            image_slider(driver, "//button[contains(@class, 'absolute left-2')]", steps=num_images, direction="left")

            # Step 4: Close the image slider
            close_slider(driver)

        # Step 5: Click category sections
        click_categories(driver)

        print("\nAll actions completed successfully!")

    except:
        print(f"Error encountered: ")
    finally:
        time.sleep(3)
        driver.quit()

# Run the script
main();
