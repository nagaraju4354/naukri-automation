# Naukri Automation — Login & Edit Profile

## Project Structure
```
naukri_automation/
├── tests/
│   └── naukri_login_profile.robot   # Main test suite
├── resources/
│   └── naukri.resource              # Shared keywords & variables
├── pages/
│   ├── login_page.py                # Login POM class
│   └── profile_page.py              # Profile POM class
├── locators/
│   └── naukri_locators.py           # All locators
└── requirements.txt
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install ChromeDriver (auto-managed)
pip install webdriver-manager
```

## Run Tests

```bash
# Run all tests
robot tests/naukri_login_profile.robot

# Run single test case by tag
robot --include smoke tests/naukri_login_profile.robot

# Run with HTML report output
robot --outputdir results tests/naukri_login_profile.robot
```

## Test Cases
| TC ID   | Name                                      | Tags              |
|---------|-------------------------------------------|-------------------|
| TC_001  | Open Naukri Application & Verify Homepage | smoke, homepage   |
| TC_002  | Login With Valid Credentials              | smoke, login      |
| TC_003  | Navigate To Edit Profile Page             | smoke, profile    |

## Notes
- Ensure Chrome browser is installed
- Tests use explicit waits — no time.sleep()
- Page Objects follow POM pattern (locators separated from logic)
