from behave import given, when, then, step
from selenium.webdriver.support.ui import Select
from support.helpers import find_element, wait_for_elements, wait_for_url_contains
from support.locators import InventoryPageLocators

@given('le texte du sélecteur de tri affiche "{sort_option}"')
def step_given_sort_option_displayed(context, sort_option):
    sort_selector = find_element(context.browser, InventoryPageLocators.SORT_SELECTOR)
    assert sort_selector is not None, "Le sélecteur de tri n'est pas trouvé"

    select = Select(sort_selector)
    actual_option = select.first_selected_option.text

    assert actual_option == sort_option, f"Option de tri attendue : '{sort_option}', Option actuelle : '{actual_option}'"

@step('je sélectionne l\'option de tri "{sort_option}"')
def step_when_select_sort_option(context, sort_option):
    sort_selector = find_element(context.browser, InventoryPageLocators.SORT_SELECTOR)
    assert sort_selector is not None, "Le sélecteur de tri n'est pas trouvé"
    select = Select(sort_selector)
    select.select_by_visible_text(sort_option)

@then('les produits avec leurs noms sont affichés dans cet ordre :')
def step_then_products_sorted(context):
    expected_order = [row['nom_produit'] for row in context.table]
    product_name_elements = wait_for_elements(context.browser, InventoryPageLocators.PRODUCT_NAME)
    actual_order = [elem.text.strip() for elem in product_name_elements]

    assert actual_order == expected_order, f"Ordre attendu : {expected_order}, Ordre actuel : {actual_order}"

@then('les produits avec leurs noms et leurs prix sont affichés dans cet ordre :')
def step_then_products_sorted_with_prices(context):
    expected_order = [(row['nom_produit'], row['prix']) for row in context.table]
    product_elements = wait_for_elements(context.browser, InventoryPageLocators.INVENTORY_ITEMS)

    actual_order = []
    for elem in product_elements:
        name_elem = elem.find_element(*InventoryPageLocators.PRODUCT_NAME)
        price_elem = elem.find_element(*InventoryPageLocators.PRODUCT_PRICE)
        actual_order.append((name_elem.text.strip(), price_elem.text.strip()))

    assert actual_order == expected_order, f"Ordre attendu : {expected_order}, Ordre actuel : {actual_order}"

