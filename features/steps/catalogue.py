from behave import given, when, then
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import find_element, wait_for_element, wait_for_elements, click_element, send_keys_to_element, wait_for_url_contains, login

# Précondition : Connexion préalable
@given('je suis connecté avec "{username}" et "{password}"')
def step_given_logged_in(context, username, password):
    login(context.browser, username, password)

# Scenario: TC-CAT-35 - Accès détail produit via le nom
@given('je suis connecté sur la page "{page_name}"')
def step_given_connected_on_page(context, page_name):
    if page_name == "/inventory.html":
        context.browser.get("https://www.saucedemo.com/inventory.html")
        wait_for_url_contains(context.browser, "inventory.html")
    else:
        raise ValueError(f"Page inconnue : {page_name}")
  
@when('je clique sur le nom du produit "{product_name}"')
def step_when_click_on_product_name(context, product_name):
    product_element = find_element(context.browser, (By.XPATH, f"//div[@class='inventory_item_name' and text()='{product_name}']"))
    assert product_element is not None, f"Produit '{product_name}' non trouvé"
    click_element(context.browser, product_element)

@then('je suis redirigé vers la fiche produit "{link_product}"')
def step_then_redirected_to_product_page(context, link_product):
    wait_for_url_contains(context.browser, link_product)
    current_url = context.browser.current_url
    assert link_product in current_url, f"URL actuelle '{current_url}' ne contient pas '{link_product}'"