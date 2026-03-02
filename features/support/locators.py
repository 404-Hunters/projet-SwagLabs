"""
Locators pour les éléments de la page SwagLabs
"""
from selenium.webdriver.common.by import By


class LoginPageLocators:
    """Locators pour la page de connexion"""
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    SUCCESS_MSG = (By.CSS_SELECTOR, "div.flash.success")
    FORM = (By.CSS_SELECTOR, "form")


class InventoryPageLocators:
    """Locators pour la page catalogue/inventaire"""
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[class*='btn_inventory']")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_SELECTOR = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    OPTION_ELEMENT = (By.XPATH, "//option[text()='{}']")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
class CartPageLocators:
    """Locators pour la page panier"""
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[class*='cart_button']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")


class CheckoutPageLocators:
    """Locators pour les pages de checkout"""
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
