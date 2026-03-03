"""
Package support pour les utilitaires Selenium
"""
from .locators import (
    LoginPageLocators,
    InventoryPageLocators,
    CartPageLocators,
    CheckoutPageLocators,
    ProductDetailPageLocators,
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
]
