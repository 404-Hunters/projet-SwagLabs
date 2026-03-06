from behave import given, when, then
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import find_element, wait_for_element, wait_for_elements, wait_for_element_clickable, wait_for_element_visible, click_element, send_keys_to_element, wait_for_url_contains
from support.locators import LoginPageLocators, InventoryPageLocators


@given('l\'utilisateur est sur la page Login')
def step_open_login_page(context):
    context.browser.get("https://www.saucedemo.com/")

@when('l\'utilisateur saisit "{text}" dans le champ "{field_name}"')
def step_enter_text_in_field(context, text, field_name):
    logging.info(f"Tentative de saisie de '{text}' dans {field_name}")

    if field_name == "Username":
        field = wait_for_element_visible(context.browser, LoginPageLocators.USERNAME_INPUT)
    elif field_name == "Password":
        field = wait_for_element_visible(context.browser, LoginPageLocators.PASSWORD_INPUT)
    else:
        raise ValueError(f"Champ inconnu : {field_name}")
    
    assert field is not None, f"Champ {field_name} non trouvé"
    
    field.clear()
    field.send_keys(text)

    actual_value = field.get_attribute("value")
    assert actual_value == text, \
        f"Valeur attendue '{text}', trouvée '{actual_value}'"
    
    logging.info(f"✅ '{text}' correctement saisi dans {field_name}")

# Pour les champs vides
@when('l\'utilisateur laisse le champ "{field_name}" vide')
def step_leave_field_empty(context, field_name):
    logging.info(f"Tentative de laisser le champ {field_name} vide")

    if field_name == "Username":
        field = wait_for_element_visible(context.browser, LoginPageLocators.USERNAME_INPUT)
    elif field_name == "Password":
        field = wait_for_element_visible(context.browser, LoginPageLocators.PASSWORD_INPUT)
    else:
        raise ValueError(f"Champ inconnu : {field_name}")
    
    assert field is not None, f"Champ {field_name} non trouvé"
    
    field.clear()

    actual_value = field.get_attribute("value")
    assert actual_value == "", f"Le champ {field_name} n'est pas vide"

    logging.info(f"✅ Le champ {field_name} est bien vide")

@when('l\'utilisateur clique sur le bouton "{button_name}"')
def step_click_button(context, button_name):
    if button_name == "Login":
        button = wait_for_element_clickable(context.browser, LoginPageLocators.LOGIN_BUTTON)
        assert button is not None, f"Bouton {button_name} non trouvé"
        button.click()
    else:
        raise ValueError(f"Bouton inconnu : {button_name}")
    
def step_verify_url(context, expected_path):

    assert wait_for_url_contains(context.browser, expected_path), \
        f"URL attendue : {expected_path}, URL actuelle : {context.browser.current_url}"

@then('la liste des produits est affichée')
def step_verify_products_displayed(context):

    products = wait_for_elements(context.browser, InventoryPageLocators.INVENTORY_ITEMS)
    
    assert len(products) > 0, "Aucun produit trouvé sur la page"

@then('l\'utilisateur reste sur la page Login')
def step_verify_stay_on_login_page(context):
    assert wait_for_url_contains(context.browser, "saucedemo.com"), "L'utilisateur n'est pas resté sur la page Login"

# pour locked_out_user un message d'erreur : 
@then('le message d\'erreur "{expected_error}" est affiché')
def step_verify_locked_out_error(context, expected_error):
    error_message = wait_for_element(context.browser, LoginPageLocators.ERROR_MESSAGE)
    assert error_message is not None, "Message d'erreur non trouvé"
    assert expected_error in error_message.text

# ================================================ #
# FEATURE : Authentification - Déconnexion (Logout)
# ================================================ #

# Connecté en tant que "standard_user"
@given('l\'utilisateur est connecté en tant que "{username}"')
def step_login_as_user(context, username):
    context.browser.get("https://www.saucedemo.com/")
    step_enter_text_in_field(context, username, "Username")
    step_enter_text_in_field(context, "secret_sauce", "Password")
    step_click_button(context, "Login")
    step_verify_url(context, "inventory.html")

@when('l\'utilisateur clique sur le menu "{menu_name}"')
def step_click_menu(context, menu_name):
    if menu_name == "Burger":
        click_element(context.browser, InventoryPageLocators.BURGER_MENU_BUTTON)
    else:
        raise ValueError(f"Menu inconnu : {menu_name}")

@when('l\'utilisateur clique sur le lien "{link_name}"')
def step_click_link(context, link_name):
    if link_name == "Logout":
        click_element(context.browser, InventoryPageLocators.LOGOUT_LINK)
    else:
        raise ValueError(f"Lien inconnu : {link_name}")
    

@then('l\'utilisateur est redirigé vers la page Login')
def step_verify_redirect_to_login(context):
    step_verify_url(context, "saucedemo.com")



