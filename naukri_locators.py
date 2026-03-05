from selenium.webdriver.common.by import By


class NaukriLocators:
    # Login Page
    LOGIN_BUTTON_NAV     = (By.XPATH, "//a[contains(@href,'login') and contains(text(),'Login')]")
    EMAIL_FIELD          = (By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")
    PASSWORD_FIELD       = (By.XPATH, "//input[@placeholder='Enter your password']")
    SUBMIT_BUTTON        = (By.XPATH, "//button[@type='submit' and contains(text(),'Login')]")
    LOGIN_ERROR_MSG      = (By.XPATH, "//div[contains(@class,'errrorMessage') or contains(@class,'error-msg')]")

    # Post-Login
    USER_AVATAR          = (By.XPATH, "//div[contains(@class,'nI-gNb-drawer__icon')]")
    VIEW_PROFILE_LINK    = (By.XPATH, "//a[contains(text(),'View & Update Profile')]")
    PROFILE_DROPDOWN     = (By.XPATH, "//div[contains(@class,'nI-gNb-lg')]//span[contains(@class,'nI-gNb-dpd-icon')]")

    # Edit Profile Page
    EDIT_PROFILE_ICON    = (By.XPATH, "//span[contains(@class,'edit-icon') or contains(@class,'editIcon')]")
    PROFILE_NAME         = (By.XPATH, "//div[contains(@class,'name-heading') or contains(@class,'nameHeading')]")
    RESUME_HEADLINE      = (By.ID, "resumeHeadlineTxt")
    SAVE_BUTTON          = (By.XPATH, "//button[contains(text(),'Save')]")
