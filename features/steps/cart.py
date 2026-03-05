from behave import given, when, then, step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from support.helpers import find_element, find_elements, wait_for_element, wait_for_element_visible, wait_for_element_clickable, wait_for_elements, wait_for_url_contains, localiser_produit_par_nom, localiser_cta_produit, click_bouton_link_panier
from support.locators import InventoryPageLocators, ProductPageLocators, CartPageLocators, CheckoutPageLocators


# Scenario TC-CART-01 : Ajout d'un produit depuis la page Inventory

@step('le bouton de l\'article "{product_name}" affiche "{expected_text}"')
def step_verification_affichage_cta_produit_inventory(context, product_name, expected_text):
    button_element = localiser_cta_produit(context, product_name)
    assert button_element is not None, f"Le bouton de l'article '{product_name}' n'a pas été trouvé"
    assert button_element.text.strip() == expected_text, f"Le bouton de l'article '{product_name}' n'affiche pas '{expected_text}', mais '{button_element.text.strip()}'"


@step('le bouton de l\'article "{product_name}" sur la page détail affiche "{expected_text}"')
def step_verification_affichage_fiche_detail(context, product_name, expected_text):
    button_element = wait_for_element_clickable(context.browser, ProductPageLocators.CTA_BUTTON)
    assert button_element is not None, "Le bouton 'Add to cart' sur la fiche détail n'a pas été trouvé"
    assert button_element.text.strip() == expected_text, f"Le bouton n'affiche pas '{expected_text}', mais '{button_element.text.strip()}'"


@then('le badge rouge du panier affiche "{expected_badge_count:d}"')
def step_verification_badge_count(context, expected_badge_count):
    xpath = "//a[@class='shopping_cart_link']//span[@class='shopping_cart_badge' and @data-test='shopping-cart-badge']"
    badge_element = wait_for_element_visible(context.browser, (By.XPATH, xpath))
    assert badge_element is not None, "Le badge rouge du panier n'a pas été trouvé"
    actual_badge_count = badge_element.text.strip()
    assert actual_badge_count == str(expected_badge_count), f"Le badge rouge du panier affiche '{actual_badge_count}', attendu '{expected_badge_count}'"


@then('le panier contient l\'article "{product_name}"')
def step_verification_article_panier(context, product_name):
    # Trouver l'article dans le panier
    article_element = localiser_produit_par_nom(context, product_name)
    assert article_element is not None, f"L'article '{product_name}' n'est pas présent dans le panier"

# Scenario TC-CART-02 : Ajout d'un produit depuis la fiche détail
@given('l\'utilisateur est sur la page de détail du produit "{product_name}"')
def step_naviguer_page_detail(context, product_name):
    product_element_name = localiser_produit_par_nom(context, product_name).find_element(*InventoryPageLocators.PRODUCT_NAME)
    # Cliquer sur le produit pour accéder à sa fiche détail
    assert product_element_name is not None, f"Produit '{product_name}' non trouvé sur la page Inventory"
    product_element_name.click()
    # Vérifier que l'URL contient "/inventory-item.html"
    wait_for_url_contains(context.browser, "/inventory-item.html")

@when('l\'utilisateur clique sur le bouton "Add to cart" depuis la fiche détail')
def step_ajout_panier_fiche_detail(context):
    button_element = wait_for_element(context.browser, ProductPageLocators.CTA_BUTTON)
    assert button_element is not None, "Le bouton 'Add to cart' sur la fiche détail n'a pas été trouvé"
    button_element.click()

#Scenario Ajout de tous les produits (6 articles)
@given('le panier est vide')
def step_vider_panier(context):
    # Vérifier que le panier est vide en cliquant sur l'icône du panier et en vérifiant qu'il est vide
    cart_badge_element = find_element(context.browser, InventoryPageLocators.SHOPPING_CART_BADGE)
    assert cart_badge_element is None, "Le panier n'est pas vide, le badge rouge est présent avec un nombre de produits"


@when('l\'utilisateur clique sur "Add to cart" pour chacun des {product_count:d} produits disponibles')
def step_ajout_tous_produits(context, product_count):
    # Trouver tous les produits sur la page
    products = find_elements(context.browser, InventoryPageLocators.INVENTORY_ITEMS)
    assert len(products) == product_count, f"Le nombre de produits n'est pas égal à {product_count}, mais à {len(products)}"
    # Cliquer sur le bouton "Add to cart" pour chaque produit
    for product in products:
        button = product.find_element(*InventoryPageLocators.ADD_TO_CART_BUTTON)
        assert button is not None, f"Le bouton 'Add to cart' pour le produit '{product.find_element(InventoryPageLocators.PRODUCT_NAME).text}' n'a pas été trouvé"
        button.click()

@then('tous les boutons des produits affichent "{expected_text}"')
def step_verification_texte_remove_boutons(context, expected_text):
    # Trouver tous les boutons "Remove" sur la page
    buttons = wait_for_elements(context.browser, InventoryPageLocators.CTA_BUTTON)
    for button in buttons:
        assert button is not None, "Un bouton 'Remove' n'a pas été trouvé"
        assert button.text.strip() == expected_text, f"Le bouton n'affiche pas '{expected_text}', mais '{button.text.strip()}'"

@when('l\'utilisateur clique sur l\'icône du panier')
def step_click_panier(context):
    click_bouton_link_panier(context)

@then('l\'utilisateur est redirigé vers la page Panier "{expected_url}"')
def step_verification_redirection_panier(context, expected_url):
    assert wait_for_url_contains(context.browser, expected_url), f"URL attendue : '{expected_url}', URL actuelle : '{context.browser.current_url}'"

@then('le panier contient exactement {expected_count:d} produits')
def step_verification_nombre_produits_panier(context, expected_count):
    cart_items = wait_for_elements(context.browser, CartPageLocators.CART_ITEM)
    assert cart_items is not None, "Les éléments du panier n'ont pas été trouvés"
    actual_count = len(cart_items)
    assert actual_count == expected_count, f"Le panier contient {actual_count} produits, attendu {expected_count}"


#TC-CART-05: Suppression d'un article depuis la page d'accueil
@then('le badge du panier disparaît')
def step_verification_badge_disparition(context):
    cart_badge_element = find_element(context.browser, InventoryPageLocators.SHOPPING_CART_BADGE)
    assert cart_badge_element is None, "Le badge du panier n'est pas supprimé"

@then('le panier est vide')
def step_verification_panier_vide(context):
    # Cliquer sur l'icône du panier pour accéder à la page du panier
    click_bouton_link_panier(context)
    wait_for_url_contains(context.browser, "/cart.html")
    cart_items = find_elements(context.browser, CartPageLocators.CART_ITEM)
    assert cart_items is None or len(cart_items) == 0, "Le panier n'est pas vide"

# TC-CART-06 : Suppression d'un produit du panier
@then('l\'article "{product_name}" est retiré de la liste du panier')
def step_verification_article_retiré_panier(context, product_name):
    # Vérifier que l'article n'est plus présent dans le panier
    cart_item = find_element(context.browser, (By.XPATH, f"//div[@data-test='cart-item-name' and text()='{product_name}']"))
    assert cart_item is None, f"L'article '{product_name}' est toujours présent dans le panier"