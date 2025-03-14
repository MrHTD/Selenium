from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up WebDriver
options = Options()
options.add_argument("--incognito")
# Bypass bot detection
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")  # Open browser in fullscreen
options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the target page
driver.get("https://mawrid.user.devxonic.com")

# Wait for the page to load completely
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body")))


def scroll_to_element(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)  # Allow animation


def navigate_swiper(driver, button_xpath, direction="next"):
    slide_index = 1
    while True:
        try:
            # Wait for the button to be clickable
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            if button.get_attribute("aria-disabled") == "true":
                print(f"Reached the last slide in {direction} direction.")
                break

            print(f"{direction.capitalize()} button found and enabled. Clicking...")
            scroll_to_element(driver, button)

            # Try clicking normally
            try:
                button.click()
            except ElementNotInteractableException:
                print(f"Regular click failed. Trying JavaScript click...")
                driver.execute_script("arguments[0].click();", button)

            slide_index += 1 if direction == "next" else -1
        except NoSuchElementException:
            print(
                f"{direction.capitalize()} button is no longer visible. Stopping navigation.")
            break
        except Exception as e:
            print(f"Error during {direction} navigation: {e}")
            break

    print(f"Swiper navigation in {direction} direction successful!")


try:
    # Step 01: Wait for the Swiper section to be present
    swiper_section = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'relative w-full')]"))
    )
    scroll_to_element(driver, swiper_section)

    # Step 02: Navigate forward through Swiper slides
    navigate_swiper(
        driver, "//button[contains(@class, 'custom-swiper-next')]", direction="next")

    # Step 03: Navigate backward through Swiper slides
    navigate_swiper(
        driver, "//button[contains(@class, 'custom-swiper-prev')]", direction="prev")

    # Step 04: Locate all cards after Swiper navigation
    cards = driver.find_elements(
        By.XPATH, "//div[contains(@class, 'swiper-slide')]//div[contains(@class, 'grid')]//div[contains(@class, 'overflow-hidden row-span-1')]//div[contains(@class, 'p-2 flex')]")

    # Step 05: Iterate through each card and find the one with the desired content
    if cards:
        # Select the first card
        card = cards[0]
        try:
            # Locate the "scan" button within this card
            scan_button = card.find_element(
                By.XPATH, ".//div[contains(@class, 'cursor-pointer')]")

            scroll_to_element(driver, scan_button) # Ensure the button is in view

            # Debugging: Print scan button details
            print(f"Scan button displayed: {scan_button.is_displayed()}")
            print(f"Scan button enabled: {scan_button.is_enabled()}")
            print(f"Scan button location: {scan_button.location}")
            print(f"Scan button size: {scan_button.size}")

            # Wait for the button to be clickable
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((scan_button))
            )

            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(scan_button))


            # Try clicking normally
            try:
                scan_button.click()
            except ElementNotInteractableException:
                print(f"Regular click failed. Trying JavaScript click...")
                driver.execute_script("arguments[0].click();", button)

        except NoSuchElementException:
            print("Product name or scan button not found in this card.")
        except Exception as e:
            print(f"Error processing card: {e}")

    print("Swiper navigation and scan button click successful!")

except Exception as e:
    print("Swiper navigation failed:", e)

# Wait before closing
time.sleep(3)
driver.quit()
