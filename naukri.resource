*** Settings ***
Library    SeleniumLibrary    timeout=15s    implicit_wait=0s
Library    OperatingSystem

*** Variables ***
${BROWSER}          chrome
${NAUKRI_URL}       https://www.naukri.com
${PROFILE_URL}      https://www.naukri.com/mnjuser/profile
${USERNAME}         nagaraju.251n@gmail.com
${PASSWORD}         Idntknow
${TIMEOUT}          15s

# Login Locators
${LOGIN_BTN_NAV}        xpath=//a[contains(@href,'login') and contains(text(),'Login')]
${EMAIL_FIELD}          xpath=//input[@placeholder='Enter your active Email ID / Username']
${PASSWORD_FIELD}       xpath=//input[@placeholder='Enter your password']
${SUBMIT_BTN}           xpath=//button[@type='submit' and contains(text(),'Login')]

# Profile Locators
${USER_AVATAR}          xpath=//div[contains(@class,'nI-gNb-drawer__icon')]
${VIEW_PROFILE_LINK}    xpath=//a[contains(text(),'View & Update Profile')]
${PROFILE_PAGE_HEADING}    xpath=//div[contains(@class,'name-heading') or contains(@class,'nameHeading') or contains(@class,'profileName')]
${EDIT_PENCIL_ICON}     xpath=//em[contains(@class,'icon edit')]

# Edit Form Locators
${UPDATED_NAME}          Naga Raju Kottu
${NAME_FIELD}            xpath=//input[@name='name' or @id='name' or contains(@placeholder,'Name') or contains(@placeholder,'name')]
${FIRST_NAME_FIELD}      xpath=//input[@name='firstName' or @id='firstName' or contains(@placeholder,'First Name') or contains(@placeholder,'first name')]
${SAVE_BTN}             xpath=//button[normalize-space(text())='Save' or normalize-space(text())='Save Changes'] | //button[@type='submit' and (contains(@class,'save') or contains(@class,'Save'))]

# AI Chat Popup Locators
${AI_CHAT_CLOSE_BTN}    xpath=//button[contains(@class,'closeBtn') or contains(@class,'close-btn') or contains(@aria-label,'Close') or contains(@class,'botCloseIcon') or contains(@id,'close')]
${AI_CHAT_POPUP}        xpath=//div[contains(@class,'botInterface') or contains(@class,'chatbot') or contains(@class,'aiBanner') or contains(@id,'bot') or contains(@class,'naukri-bot')]

*** Keywords ***
Open Naukri Browser
    [Documentation]    Launch Chrome and open Naukri homepage
    Open Browser    ${NAUKRI_URL}    ${BROWSER}    options=add_argument("--headless=new");add_argument("--no-sandbox");add_argument("--disable-dev-shm-usage");add_argument("--window-size=1920,1080")
    Set Selenium Timeout    ${TIMEOUT}
    Log    Browser opened: ${NAUKRI_URL}

Click Login Nav Button
    [Documentation]    Click the Login button in the top navigation bar
    Wait Until Element Is Visible    ${LOGIN_BTN_NAV}    timeout=${TIMEOUT}
    Click Element    ${LOGIN_BTN_NAV}
    Log    Clicked Login nav button

Enter Login Credentials
    [Documentation]    Fill in email and password fields
    [Arguments]    ${email}    ${password}
    Wait Until Element Is Visible    ${EMAIL_FIELD}       timeout=${TIMEOUT}
    Clear Element Text               ${EMAIL_FIELD}
    Input Text                       ${EMAIL_FIELD}       ${email}
    Wait Until Element Is Visible    ${PASSWORD_FIELD}    timeout=${TIMEOUT}
    Clear Element Text               ${PASSWORD_FIELD}
    Input Text                       ${PASSWORD_FIELD}    ${password}
    Log    Credentials entered for: ${email}

Submit Login Form
    [Documentation]    Click the Login submit button
    Wait Until Element Is Enabled    ${SUBMIT_BTN}    timeout=${TIMEOUT}
    Click Element                    ${SUBMIT_BTN}
    Log    Login form submitted

Close AI Chat Popup If Present
    [Documentation]    Closes the AI chat/bot popup if it appears after login
    ${popup_visible}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${AI_CHAT_POPUP}    timeout=5s
    IF    ${popup_visible}
        Log    AI chat popup detected — attempting to close
        ${close_btn_visible}=    Run Keyword And Return Status
        ...    Wait Until Element Is Visible    ${AI_CHAT_CLOSE_BTN}    timeout=5s
        IF    ${close_btn_visible}
            Click Element    ${AI_CHAT_CLOSE_BTN}
            Log    ✅ AI chat popup closed successfully
        ELSE
            Press Keys    None    ESCAPE
            Log    ✅ AI chat popup dismissed via ESC key
        END
    ELSE
        Log    No AI chat popup detected — continuing
    END

Login To Naukri
    [Documentation]    Full login flow: nav click → credentials → submit → close popup
    [Arguments]    ${email}=${USERNAME}    ${password}=${PASSWORD}
    Click Login Nav Button
    Enter Login Credentials    ${email}    ${password}
    Submit Login Form
    Wait Until Location Contains    naukri.com    timeout=20s
    Close AI Chat Popup If Present
    Log    ✅ Successfully logged in as ${email}

Click View Profile
    [Documentation]    Click user avatar then click View & Update Profile link
    Wait Until Element Is Visible    ${USER_AVATAR}         timeout=${TIMEOUT}
    Click Element                    ${USER_AVATAR}
    Wait Until Element Is Visible    ${VIEW_PROFILE_LINK}   timeout=${TIMEOUT}
    Click Element                    ${VIEW_PROFILE_LINK}
    Wait Until Location Contains     profile                timeout=${TIMEOUT}
    Log    ✅ Clicked View Profile — now on profile page

Click Edit Pencil Icon
    [Documentation]    Click the pencil/edit icon next to name on profile page
    # Try direct visible click first
    ${clicked}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${EDIT_PENCIL_ICON}    timeout=8s
    IF    ${clicked}
        Click Element    ${EDIT_PENCIL_ICON}
        Log    ✅ Clicked pencil icon via standard click
    ELSE
        # Fallback: JavaScript click on any edit icon near the name
        Execute Javascript    document.querySelector("em.icon.edit").click()
        Log    ✅ Clicked pencil icon via JavaScript fallback
    END
    Log    ✅ Edit pencil icon clicked — form should be open now

Update Name And Save
    [Documentation]    Clear name field, enter new name and click Save
    [Arguments]    ${new_name}=${UPDATED_NAME}
    ${name_visible}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible    ${NAME_FIELD}    timeout=8s
    IF    ${name_visible}
       # Triple Click Element    ${NAME_FIELD}
        Clear Element text     ${NAME_FIELD}
        Input Text              ${NAME_FIELD}    ${new_name}
        Log    ✅ Entered name: ${new_name}
    ELSE
        Wait Until Element Is Visible    ${FIRST_NAME_FIELD}    timeout=8s
        #Triple Click Element             ${FIRST_NAME_FIELD}
        Input Text                       ${FIRST_NAME_FIELD}    ${new_name}
        Log    ✅ Entered name in first name field: ${new_name}
    END
    Wait Until Element Is Visible    ${SAVE_BTN}    timeout=${TIMEOUT}
    Click Element                    ${SAVE_BTN}
    Log    ✅ Clicked Save — name updated to: ${new_name}

Navigate To Edit Profile
    [Documentation]    Go to the profile edit page directly via URL
    Go To    ${PROFILE_URL}
    Wait Until Location Contains    profile    timeout=${TIMEOUT}
    Log    Navigated to Edit Profile page

Verify Edit Profile Page Is Open
    [Documentation]    Assert we are on the profile edit page
    Location Should Contain    profile
    Log    Verified: Edit Profile page is open

Close Naukri Browser
    [Documentation]    Close all browser windows
    Close All Browsers
    Log    Browser closed
