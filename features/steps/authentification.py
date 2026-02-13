from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import find_element, wait_for_element, wait_for_elements, click_element, send_keys_to_element, wait_for_url_contains


@given('je suis sur la page Login')
def step_open_login_page(context):
    context.browser.get("https://www.saucedemo.com/")

@when('je saisis "{text}" dans le champ "{field_name}"')
def step_enter_text_in_field(context, text, field_name):
    if field_name == "Username":
        field = find_element(context.browser, (By.ID, "user-name"))
    elif field_name == "Password":
        field = find_element(context.browser, (By.ID, "password"))
    else:
        raise ValueError(f"Champ inconnu : {field_name}")
    
    assert field is not None, f"Champ {field_name} non trouvé"
    
    field.clear()
    field.send_keys(text)

@when('je clique sur le bouton "{button_name}"')
def step_click_button(context, button_name):
    if button_name == "Login":
        button = find_element(context.browser, (By.ID, "login-button"))
        assert button is not None, f"Bouton {button_name} non trouvé"
        button.click()
    else:
        raise ValueError(f"Bouton inconnu : {button_name}")

@then('je suis redirigé vers la page "{expected_path}"')
def step_verify_url(context, expected_path):

    assert wait_for_url_contains(context.browser, expected_path), \
        f"URL attendue : {expected_path}, URL actuelle : {context.browser.current_url}"

@then('la liste des produits est affichée')
def step_verify_products_displayed(context):

    products = wait_for_elements(context.browser, (By.CLASS_NAME, "inventory_item"))
    
    assert len(products) > 0, "Aucun produit trouvé sur la page"