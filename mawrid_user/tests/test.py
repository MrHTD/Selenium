from pages.login import LoginPage
from pages.home_page import HomePage
from pages.add_to_cart import CartPage
from pages.signup import SignupPage
from utils.config import Config

def test(browser):
    # Initialize pages
    login_page = LoginPage(browser)
    signup = SignupPage(browser)
    home_page = HomePage(browser)
    cart_page = CartPage(browser)

    # Execute flow
    browser.get(Config.BASE_URL)
    login_page.login(Config.VALID_EMAIL, Config.VALID_PASSWORD)