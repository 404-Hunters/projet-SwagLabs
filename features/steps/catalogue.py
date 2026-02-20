from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.helpers import find_element, wait_for_element, wait_for_elements, click_element, send_keys_to_element, wait_for_url_contains, login, wait_for_element_clickable

# Scenario: TC-CAT-35 - Accès détail produit via le nom
@given('je suis sur la page "{page_name}"')
def step_given_connected_on_page(context, page_name):
    if page_name == "/inventory.html":
        context.browser.get("https://www.saucedemo.com/inventory.html")
        wait_for_url_contains(context.browser, "inventory.html")
    else:
        raise ValueError(f"Page inconnue : {page_name}")
  
@when('je clique sur le nom du produit "{product_name}"')
def step_when_click_on_product_name(context, product_name):
    product_link = find_element(context.browser, (By.ID, "item_4_title_link"))
    assert product_link is not None, f"Le lien du produit '{product_name}' n'est pas cliquable ou introuvable"

    print(f"Élément trouvé : {product_link.tag_name}")

    # Clic via JS pour déclencher l'event listener
    context.browser.execute_script("arguments[0].click();", product_link)

@then('je suis redirigé vers la fiche produit "{link_product}"')
def step_then_redirected_to_product_page(context, link_product):
    assert wait_for_url_contains(context.browser, link_product), \
        f"URL attendue : {link_product}, URL actuelle : {context.browser.current_url}"
    
@then('le nom "{product_name}" est affiché')
def step_then_product_name_displayed(context, product_name):
    name_element = find_element(context.browser, (By.CLASS_NAME, "inventory_details_name"))
    assert name_element is not None, "Élément du nom du produit non trouvé"
    actual_name = name_element.text
    assert actual_name == product_name, f"Nom attendu : '{product_name}', Nom actuel : '{actual_name}'"

@then('le prix "{product_price}" est visible')
def step_then_product_price_visible(context, product_price):
    price_element = find_element(context.browser, (By.CLASS_NAME, "inventory_details_price"))
    assert price_element is not None, "Élément du prix du produit non trouvé"
    actual_price = price_element.text
    assert actual_price == product_price, f"Prix attendu : '{product_price}', Prix actuel : '{actual_price}'"

@then('l\'image agrandie du produit est visible avec le alt "{alt_text}"')
def step_then_product_image_visible(context, alt_text):
    image_element = find_element(context.browser, (By.CLASS_NAME, "inventory_details_img"))
    assert image_element is not None, "Élément de l'image du produit non trouvé"
    actual_alt = image_element.get_attribute("alt")
    assert actual_alt == alt_text, f"Alt attendu : '{alt_text}', Alt actuel : '{actual_alt}'"

@then('la description du produit est affichée')
def step_then_product_description_displayed(context):
    description_element = find_element(context.browser, (By.CLASS_NAME, "inventory_details_desc"))
    assert description_element is not None, "Élément de la description du produit non trouvé"
    assert description_element.text != "", "La description du produit est vide"

# scenario: TC-CAT-34 - Accès détail produit via l'image
@when('je clique sur l\'image du produit "{product_name}"')
def step_when_click_on_product_image(context, product_name):
    product_image = find_element(context.browser, (By.ID, "item_4_img_link"))
    assert product_image is not None, f"L'image du produit '{product_name}' n'est pas cliquable ou introuvable"

    print(f"Élément trouvé : {product_image.tag_name}")

    # Clic via JS pour déclencher l'event listener
    context.browser.execute_script("arguments[0].click();", product_image)