from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.naukri_locators import NaukriLocators
import logging

logger = logging.getLogger(__name__)


class LoginPage:
    BASE_URL = "https://www.naukri.com"

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        logger.info("Navigating to Naukri homepage")
        self.driver.get(self.BASE_URL)
        self.driver.maximize_window()

    def click_login_nav(self):
        logger.info("Clicking Login button in navigation")
        btn = self.wait.until(EC.element_to_be_clickable(NaukriLocators.LOGIN_BUTTON_NAV))
        btn.click()

    def enter_email(self, email):
        logger.info(f"Entering email: {email}")
        field = self.wait.until(EC.visibility_of_element_located(NaukriLocators.EMAIL_FIELD))
        field.clear()
        field.send_keys(email)

    def enter_password(self, password):
        logger.info("Entering password")
        field = self.wait.until(EC.visibility_of_element_located(NaukriLocators.PASSWORD_FIELD))
        field.clear()
        field.send_keys(password)

    def click_submit(self):
        logger.info("Submitting login form")
        btn = self.wait.until(EC.element_to_be_clickable(NaukriLocators.SUBMIT_BUTTON))
        btn.click()

    def login(self, email, password):
        """High-level composite login action."""
        self.open()
        self.click_login_nav()
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        logger.info("Login form submitted")

    def get_error_message(self):
        el = self.wait.until(EC.visibility_of_element_located(NaukriLocators.LOGIN_ERROR_MSG))
        return el.text.strip()
