from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.naukri_locators import NaukriLocators
import logging

logger = logging.getLogger(__name__)


class ProfilePage:
    PROFILE_URL = "https://www.naukri.com/mnjuser/profile"

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate_to_edit_profile(self):
        """Navigate directly to the profile edit page."""
        logger.info("Navigating directly to Edit Profile page")
        self.driver.get(self.PROFILE_URL)

    def navigate_via_dropdown(self):
        """Navigate to profile via user avatar dropdown."""
        logger.info("Opening user avatar dropdown")
        avatar = self.wait.until(EC.element_to_be_clickable(NaukriLocators.USER_AVATAR))
        avatar.click()

        logger.info("Clicking 'View & Update Profile' link")
        profile_link = self.wait.until(EC.element_to_be_clickable(NaukriLocators.VIEW_PROFILE_LINK))
        profile_link.click()

    def wait_for_profile_page_load(self):
        """Wait until the profile page is fully loaded."""
        logger.info("Waiting for profile page to load")
        self.wait.until(
            lambda d: "profile" in d.current_url.lower(),
            message="Profile page URL not reached within timeout"
        )
        logger.info(f"Profile page loaded: {self.driver.current_url}")

    def get_profile_name(self):
        el = self.wait.until(EC.visibility_of_element_located(NaukriLocators.PROFILE_NAME))
        return el.text.strip()

    def is_edit_profile_page(self):
        return "profile" in self.driver.current_url.lower()
