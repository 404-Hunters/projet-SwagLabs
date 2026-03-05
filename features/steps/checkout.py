from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import find_element, wait_for_element, wait_for_element_visible, wait_for_elements, click_element, send_keys_to_element, wait_for_url_contains, login, wait_for_element_clickable, localiser_produit_par_nom, localiser_cta_produit, click_bouton_link_panier
from support.locators import CartPageLocators, CheckoutPageLocators

@when('l\'utilisateur clique sur le bouton "{button_name}" de la page Checkout {page_name}')
def step_click_button_checkout(context, button_name, page_name):
    button_selector = {
        "Continue": CheckoutPageLocators.CONTINUE_BUTTON,
        "Finish":   CheckoutPageLocators.FINISH_BUTTON,
    }
    assert button_name in button_selector, f"Bouton inconnu : {button_name}"
    is_clicked = click_element(context.browser, button_selector[button_name])
    assert is_clicked, f"Le bouton '{button_name}' n'a pas pu être cliqué"


@then('un seul message d\'erreur "{expected_error_message}" est affiché')
def step_verification_message_erreur_checkout(context, expected_error_message):
    error_message_element = wait_for_element_visible(context.browser, CheckoutPageLocators.ERROR_MESSAGE)
    assert error_message_element is not None, "Le message d'erreur n'a pas été trouvé"
    actual_error_message = error_message_element.text.strip()
    assert actual_error_message == expected_error_message, f"Message d'erreur affiché : '{actual_error_message}', attendu : '{expected_error_message}'"
    
@then('l\'utilisateur reste sur la page "{expected_page_link}"')
def step_verification_rester_page_checkout(context, expected_page_link):
    assert wait_for_url_contains(context.browser, expected_page_link), f"URL attendue : {expected_page_link}, URL actuelle : {context.browser.current_url}"

@when('l\'utilisateur remplit le formulaire de commande:')
def step_remplir_formulaire_checkout(context):

    champ_selector = {
        "First Name": CheckoutPageLocators.FIRST_NAME_INPUT,
        "Last Name": CheckoutPageLocators.LAST_NAME_INPUT,
        "Zip/Postal Code": CheckoutPageLocators.POSTAL_CODE_INPUT
    }

    for row in context.table:
        champ, valeur = row['champ'], row['valeur']
        assert champ in champ_selector, f"Champ inconnu : '{champ}'"

        input_locator = champ_selector[champ]
        entered_value = send_keys_to_element(context.browser, input_locator, valeur.strip())

        assert entered_value == valeur.strip(), (
            f"Champ '{champ}' — attendu : '{valeur.strip()}', obtenu : '{entered_value}'"
        )

@then('le message de confirmation "{expected_message}" est affiché')
def step_verification_message_confirmation_checkout(context, expected_message):
    confirmation_element = wait_for_element_visible(context.browser, CheckoutPageLocators.COMPLETE_HEADER)
    assert confirmation_element is not None, "Le message de confirmation n'a pas été trouvé"
    actual_message = confirmation_element.text.strip()
    assert actual_message == expected_message, f"Message de confirmation affiché : '{actual_message}', attendu : '{expected_message}'"