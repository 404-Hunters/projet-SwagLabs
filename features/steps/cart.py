from behave import given, when, then, step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from support.helpers import find_element, wait_for_element, wait_for_elements, wait_for_url_contains
from support.locators import InventoryPageLocators, ProductDetailPageLocators


# Scenario TC-CART-01 : Ajout d'un produit depuis la page Inventory
@when('l\'utilisateur clique sur le bouton "{button_name}" du produit "{product_name}"')
def step_impl(context, button_name, product_name):
    # Localiser le produit par son nom
    xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{product_name}' and @data-test='inventory-item-name']//ancestor::div[@class='inventory_item']"
    product_element = find_element(context.browser, (By.XPATH, xpath))
    assert product_element is not None, f"Produit '{product_name}' non trouvé sur la page Inventory"
    # Localiser le bouton à l'intérieur du produit
    button_element = product_element.find_element(By.XPATH, f".//button[contains(text(), '{button_name}')]")
    assert button_element is not None, f"Le bouton '{button_name}' pour le produit '{product_name}' n'a pas été trouvé"
    button_element.click()

@then('le bouton du produit "{product_name}" affiche "{expected_text}"')
def step_verification_affichage(context, product_name, expected_text):
    # Localiser le produit par son nom
    xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{product_name}' and @data-test='inventory-item-name']//ancestor::div[@class='inventory_item']"
    product_element = find_element(context.browser, (By.XPATH, xpath))
    assert product_element is not None, f"Produit '{product_name}' non trouvé sur la page Inventory"
    # Localiser le bouton à l'intérieur du produit
    button_element = product_element.find_element(By.XPATH, ".//button")
    assert button_element is not None, f"Le bouton pour le produit '{product_name}' n'a pas été trouvé"

    actual_text = button_element.text.strip()
    assert actual_text == expected_text, f"Le texte du bouton pour le produit '{product_name}' est '{actual_text}', attendu '{expected_text}'"

@then('le badge rouge du panier affiche {expected_badge_count}')
def step_verification_badge_count(context, expected_badge_count):
    xpath = "//a[@class='shopping_cart_link']//span[@class='shopping_cart_badge' and @data-test='shopping-cart-badge']"
    badge_element = find_element(context.browser, (By.XPATH, xpath))
    assert badge_element is not None, "Le badge rouge du panier n'a pas été trouvé"
    actual_badge_count = badge_element.text.strip()
    clean_expected = expected_badge_count.replace('"', '').strip()
    assert actual_badge_count == clean_expected, f"Le badge rouge du panier affiche '{actual_badge_count}', attendu '{clean_expected}'"


# Scenario TC-CART-02 : Ajout d'un produit depuis la fiche détail
@given('je suis sur la page de détail du produit "{product_name}"')
def step_naviguer_page_detail(context, product_name):
    # Localiser le produit par son nom
    xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{product_name}' and @data-test='inventory-item-name']"
    product_element_name = find_element(context.browser, (By.XPATH, xpath))
    # Cliquer sur le produit pour accéder à sa fiche détail
    assert product_element_name is not None, f"Produit '{product_name}' non trouvé sur la page Inventory"
    product_element_name.click()
    # Vérifier que l'URL contient "/inventory-item.html"
    wait_for_url_contains(context.browser, "/inventory-item.html")

@when('l\'utilisateur clique sur le bouton "Add to cart" depuis la fiche détail')
def step_ajout_panier_fiche_detail(context):
    button_element = find_element(context.browser, ProductDetailPageLocators.CTA_BUTTON)
    assert button_element is not None, "Le bouton 'Add to cart' sur la fiche détail n'a pas été trouvé"
    button_element.click()

@then('le bouton "Add to cart" de la fiche détail affiche "{expected_text}"')
def step_verification_affichage_fiche_detail(context, expected_text):
    button_element = find_element(context.browser, ProductDetailPageLocators.CTA_BUTTON)
    assert button_element is not None, "Le bouton 'Add to cart' sur la fiche détail n'a pas été trouvé"
    assert button_element.text.strip() == expected_text, f"Le bouton n'affiche pas '{expected_text}', mais '{button_element.text.strip()}'"









