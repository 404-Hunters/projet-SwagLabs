# features/steps/test_login.py
from behave import given, when, then
from support.locators import LoginPageLocators
from support.helpers import find_element

@given('I am on the login page')
def step_open_login_page(context):
    context.browser.get("https://the-internet.herokuapp.com/login") 

@when('I enter username "{username}"')
def step_enter_username(context, username):
    username_input = find_element(context.browser, LoginPageLocators.USERNAME_INPUT) 
    if username_input:
        username_input.send_keys(username)

@when('I enter password "{password}"')
def step_enter_password(context, password):
    password_input = find_element(context.browser, LoginPageLocators.PASSWORD_INPUT)  
    if password_input:
        password_input.send_keys(password)

@when('I click the login button')
def step_click_login(context):
    login_button = find_element(context.browser, LoginPageLocators.LOGIN_BUTTON)  
    if login_button:
        login_button.click()

@then('I should see the success message')
def step_see_success_message(context):
    success_message = find_element(context.browser, LoginPageLocators.SUCCESS_MSG)
    assert success_message is not None, "Success message not found"