*** Settings ***
Documentation     Naukri Automation — Login → View Profile → Edit → Update Name → Save
Resource          naukri.resource
Suite Setup       Open Naukri Browser
Suite Teardown    Close Naukri Browser
Test Tags         naukri    smoke

*** Variables ***
${USERNAME}    nagaraju.251n@gmail.com
${PASSWORD}    Idntknow

*** Test Cases ***

TC_001 Login Update Name And Save
    [Documentation]    Login to Naukri → Close AI popup → Click View Profile
    ...                → Click Edit pencil icon → Update Name → Click Save
    [Tags]    smoke    positive
    Login To Naukri        ${USERNAME}    ${PASSWORD}
    Click View Profile
    Capture Page Screenshot    filename=profile_page.png
    Click Edit Pencil Icon
    Update Name And Save
    Log    ✅ Name updated to 'Naga Raju Kottu' and saved successfully
