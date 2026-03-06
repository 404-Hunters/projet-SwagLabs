"""
Package support pour les utilitaires Selenium
"""
from .locators import (
    LoginPageLocators,
    InventoryPageLocators,
    CartPageLocators,
    CheckoutPageLocators,
)
from .helpers import (
    wait_for_element,
    wait_for_element_clickable,
    wait_for_element_visible,
    is_element_present,
    get_element_text,
    send_keys_to_element,
    find_element,
    find_elements,
    fill_field,
    login,
    click_element,
    wait_for_url_contains,
    localiser_produit_par_nom,
    localiser_cta_produit,
    click_bouton_link_panier,
    wait_for_text_in_element,
)



__all__ = [
    # Locators
    'LoginLocators',
    'InventoryLocators',
    'CartLocators',
    'CheckoutLocators',
    'ProductDetailPageLocators',
    # Helpers
    'wait_for_element',
    'wait_for_element_clickable',
    'wait_for_element_visible',
    'is_element_present',
    'get_element_text',
    'click_element',
    'send_keys_to_element',
    'find_element',
    'find_elements',
    'fill_field',
    'login',
    'wait_for_url_contains',
    'localiser_produit_par_nom',
    'localiser_cta_produit',
    'click_bouton_link_panier',
    'wait_for_text_in_element',
]
