from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import find_element, wait_for_element, wait_for_elements, click_element, send_keys_to_element, wait_for_url_contains, login, wait_for_element_clickable

# Scenario: TC-CAT-36 - Tri par nom (A à Z) depuis un ordre différent
@given('je suis connecté sur la page "{page_link}"')
def step_given_page_loaded(context, page_link):
    if page_link == "/inventory.html":
        context.browser.get("https://www.saucedemo.com/inventory.html")
        wait_for_url_contains(context.browser, "inventory.html")
    else:
        raise ValueError(f"Page inconnue : {page_link}")
    
