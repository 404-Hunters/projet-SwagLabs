from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import find_element, wait_for_element, wait_for_elements, wait_for_element_visible, click_element, send_keys_to_element, wait_for_url_contains, login, wait_for_element_clickable, localiser_cta_produit, click_bouton_link_panier, localiser_produit_par_nom
from support.locators import InventoryPageLocators, CartPageLocators

# Précondition : Connexion préalable
@given('l\'utilisateur est connecté avec "{username}" et "{password}"')
def step_given_logged_in(context, username, password):
    login(context.browser, username, password)

@given('l\'utilisateur est sur la page "{page_link}"')
def step_given_page_loaded(context, page_link):
    context.browser.get(f"https://www.saucedemo.com{page_link}")
    wait_for_url_contains(context.browser, page_link)

@then('l\'utilisateur est redirigé vers la page "{expected_link}"')
def step_then_redirected_to_page(context, expected_link):
    assert wait_for_url_contains(context.browser, expected_link), \
        f"URL attendue : {expected_link}, URL actuelle : {context.browser.current_url}"

@when('l\'utilisateur clique sur le bouton "{button_name}" de l\'article "{product_name}"')
def step_ajout_panier(context, button_name, product_name):
    button_cta = localiser_cta_produit(context, product_name)
    assert button_cta is not None, f"Le bouton '{button_name}' de l'article '{product_name}' n'a pas été trouvé"
    button_cta.click()


@given('l\'article "{product_name}" est présent dans le panier')
def step_article_present_panier(context, product_name):

    # Ajouter l'article au panier si ce n'est pas déjà fait
    step_ajout_panier(context, "Add to cart", product_name)

    # Vérifier que le panier contient l'article
    cart_badge_element = wait_for_element_visible(context.browser, InventoryPageLocators.SHOPPING_CART_BADGE)
    assert cart_badge_element is not None, "Le badge du panier n'est pas présent"
    actual_badge_count_integer = int(cart_badge_element.text.strip())
    assert actual_badge_count_integer > 0, "Le badge du panier n'indique pas de produits présents"
    # Vérifier que le produit est présent dans le panier
    click_bouton_link_panier(context)
    
    product_element = localiser_produit_par_nom(context, product_name)
    assert product_element is not None, f"Le produit '{product_name}' n'est pas présent dans le panier"

    product_name_element = product_element.find_element(*CartPageLocators.CART_ITEM_NAME)
    assert product_name_element is not None, f"Le nom du produit '{product_name}' n'a pas été trouvé dans le panier"
    assert product_name_element.text.strip() == product_name, f"Le nom du produit dans le panier est '{product_name_element.text.strip()}', attendu '{product_name}'"
    
    # Chercher le bouton retour au catalogue et cliquer dessus
    continue_shopping_button = wait_for_element_clickable(context.browser, CartPageLocators.CONTINUE_SHOPPING)
    assert continue_shopping_button is not None, "Le bouton 'Continue Shopping' n'a pas été trouvé sur la page du panier"
    continue_shopping_button.click()

    # Vérifier que l'utilisateur est redirigé vers la page Inventory
    wait_for_url_contains(context.browser, "/inventory.html")