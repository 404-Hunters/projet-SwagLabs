from behave import given, when, then
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import wait_for_element_visible, click_element, send_keys_to_element, wait_for_url_contains, localiser_produit_par_nom, localiser_cta_produit
from support.locators import CheckoutPageLocators

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


# Feature calcul du total de la commande

@given('le panier contient les produits suivants:')
def step_remplir_panier_produits(context):
    for row in context.table:
        product_name = row['produit']
        quantity = int(row['quantité'])
        price = float(row['prix unitaire'])

        # Localiser le produit dans la page Inventory
        product_element = localiser_produit_par_nom(context, product_name)
        assert product_element is not None, f"Produit '{product_name}' non trouvé sur la page Inventory"

        # Cliquer sur le bouton "Add to cart" autant de fois que la quantité
        button_element = localiser_cta_produit(context, product_name)
        assert button_element is not None, f"Le bouton d'ajout pour le produit '{product_name}' n'a pas été trouvé"
        
        if quantity > 0:
            button_element.click()

@then('le total des prix de la commande sans taxe affiche "{expected_total}"')
def step_verification_total_commande(context, expected_total):
    element = wait_for_element_visible(context.browser, CheckoutPageLocators.ITEM_TOTAL_PRICE)
    assert element is not None, f"L'élément sous-total est introuvable"
    actual_total = element.text.strip()
    assert expected_total in actual_total, (
        f"Sous-total attendu : '{expected_total}', affiché : '{actual_total}'"
    )
        
@then('le montant de la taxe affiche "{expected_tax}"')
def step_verification_montant_taxe(context, expected_tax):
    element = wait_for_element_visible(context.browser, CheckoutPageLocators.TAX_AMOUNT)
    assert element is not None, f"L'élément taxe est introuvable"
    actual_tax = element.text.strip()
    assert expected_tax in actual_tax, (
        f"Taxe attendue : '{expected_tax.strip()}', affichée : '{actual_tax}'"
    )

@then('le total de la commande avec taxe affiche "{expected_total_with_tax}"')
def step_verification_total_commande_avec_taxe(context, expected_total_with_tax):
    element = wait_for_element_visible(context.browser, CheckoutPageLocators.TOTAL_PRICE)
    assert element is not None, f"L'élément total avec taxe est introuvable"
    actual_total_with_tax = element.text.strip()
    assert expected_total_with_tax in actual_total_with_tax, (
        f"Total avec taxe attendu : '{expected_total_with_tax.strip()}', affiché : '{actual_total_with_tax}'"
    )