from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import find_element, wait_for_element, wait_for_elements, click_element, send_keys_to_element, wait_for_url_contains, login, wait_for_element_clickable

# Précondition : Connexion préalable
@given('je suis connecté avec "{username}" et "{password}"')
def step_given_logged_in(context, username, password):
    login(context.browser, username, password)
