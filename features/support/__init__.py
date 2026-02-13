"""
Package support pour les utilitaires Selenium
"""
from .locators import (
    LoginPageLocators,
    InventoryPageLocators,
    CartPageLocators,
    CheckoutPageLocators
)
from .helpers import (
    wait_for_element,
    wait_for_element_clickable,
    wait_for_element_visible,
    is_element_present,
    get_element_text,
    click_element,
    send_keys_to_element
)

__all__ = [
    # Locators
    'LoginLocators',
    'InventoryLocators',
    'CartLocators',
    'CheckoutLocators',
    # Helpers
    'wait_for_element',
    'wait_for_element_clickable',
    'wait_for_element_visible',
    'is_element_present',
    'get_element_text',
    'click_element',
    'send_keys_to_element',
]
