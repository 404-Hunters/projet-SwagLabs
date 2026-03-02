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

@then('le premier produit affiché est "{first_product}"')
def step_then_first_product_displayed(context, first_product):
    inventory_items = wait_for_elements(context.browser, InventoryPageLocators.INVENTORY_ITEMS)
    assert len(inventory_items) > 0, "Aucun produit trouvé après le tri"
    first_item_name = inventory_items[0].find_element(*InventoryPageLocators.PRODUCT_NAME).text
    assert first_item_name == first_product, f"Premier produit attendu : '{first_product}', Premier produit actuel : '{first_item_name}'"

@then('le troisième produit affiché est "{third_product}"')
def step_then_third_product_displayed(context, third_product):
    inventory_items = wait_for_elements(context.browser, InventoryPageLocators.INVENTORY_ITEMS)
    assert len(inventory_items) >= 3, "Moins de 3 produits trouvés après le tri"
    third_item_name = inventory_items[2].find_element(*InventoryPageLocators.PRODUCT_NAME).text
    assert third_item_name == third_product, f"Troisième produit attendu : '{third_product}', Troisième produit actuel : '{third_item_name}'"


@then('le dernier produit affiché est "{last_product}"')
def step_then_last_product_displayed(context, last_product):
    inventory_items = wait_for_elements(context.browser, InventoryPageLocators.INVENTORY_ITEMS)
    assert len(inventory_items) > 0, "Aucun produit trouvé après le tri"
    last_item_name = inventory_items[-1].find_element(*InventoryPageLocators.PRODUCT_NAME).text
    assert last_item_name == last_product, f"Dernier produit attendu : '{last_product}', Dernier produit actuel : '{last_item_name}'"