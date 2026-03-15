"""
Fonctions utilitaires pour les tests Selenium
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from support.locators import InventoryPageLocators
from selenium.webdriver.common.by import By

default_timeout = 5  # Temps d'attente par défaut pour les fonctions d'attente


def find_element(driver, locator):
    """
    Trouve un élément en utilisant un locator
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        
    Returns:
        WebElement trouvé ou None
    """
    try:
        element = driver.find_element(*locator)
        return element
    except NoSuchElementException:
        print(f"Élément non trouvé: {locator}")
        return None
    
def find_elements(driver, locator):
    """
    Trouve plusieurs éléments en utilisant un locator
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        
    Returns:
        Liste de WebElements trouvés ou liste vide
    """
    try:
        elements = driver.find_elements(*locator)
        return elements
    except NoSuchElementException:
        print(f"Aucun élément trouvé: {locator}")
        return []


def wait_for_element(driver, locator, timeout=default_timeout):
    """
    Attend qu'un élément soit présent dans le DOM et le retourne
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        timeout: Temps d'attente maximum en secondes
        
    Returns:
        WebElement trouvé ou None
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except TimeoutException:
        print(f"Élément non trouvé après {timeout} secondes: {locator}")
        return None
    

def wait_for_elements(driver, locator, timeout=default_timeout):
    """
    Attend que plusieurs éléments soient visibles
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        timeout: Temps d'attente maximum en secondes
    Returns:
        Liste de WebElements trouvés ou liste vide
    """
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )
        return elements
    except TimeoutException:
        print(f"Aucun élément visible après {timeout} secondes: {locator}")
        return []

def wait_for_element_clickable(driver, locator, timeout=default_timeout):
    """
    Attend qu'un élément soit cliquable
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        timeout: Temps d'attente maximum en secondes
        
    Returns:
        WebElement trouvé ou None
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except TimeoutException:
        print(f"Élément non cliquable après {timeout} secondes: {locator}")
        return None


def wait_for_element_visible(driver, locator, timeout=default_timeout):
    """
    Attend qu'un élément soit visible
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        timeout: Temps d'attente maximum en secondes
        
    Returns:
        WebElement trouvé ou None
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        print(f"Élément non visible après {timeout} secondes: {locator}")
        return None
    

def is_element_present(driver, locator):
    """
    Vérifie si un élément est présent dans le DOM
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        
    Returns:
        bool: True si l'élément est présent, False sinon
    """
    try:
        driver.find_element(*locator)
        return True
    except NoSuchElementException:
        return False


def get_element_text(driver, locator, timeout=default_timeout):
    """
    Récupère le texte d'un élément
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        timeout: Temps d'attente maximum en secondes
        
    Returns:
        str: Texte de l'élément ou chaîne vide
    """
    element = wait_for_element(driver, locator, timeout)
    return element.text if element else ""

def wait_for_text_in_element(driver, locator, expected_text, timeout=default_timeout):
    """
    Vérifie qu'un texte spécifique est présent dans un élément

    Returns:
        bool: True si le texte attendu est présent, False sinon
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, expected_text)
        )
    except TimeoutException:
        print(f"Le texte '{expected_text}' n'est pas présent dans l'élément {locator} après {timeout} secondes")
        return False


def click_element(driver, locator, timeout=default_timeout):
    """
    Clique sur un élément après avoir attendu qu'il soit cliquable
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        timeout: Temps d'attente maximum en secondes
        
    Returns:
        bool: True si le clic a réussi, False sinon
    """
    element = wait_for_element_clickable(driver, locator, timeout)
    if element:
        element.click()
        return True
    return False


def send_keys_to_element(driver, locator, text, timeout=default_timeout):
    """
    Envoie du texte à un élément input
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        text: Texte à envoyer
        timeout: Temps d'attente maximum en secondes
        
    Returns:
        valeur texte entrée dans le champ ou None
    """
    element = wait_for_element_visible(driver, locator, timeout)
    if element:
        element.clear()
        element.send_keys(text)
        return element.get_attribute("value")
    return None

def wait_for_url_contains(driver, expected_url_part, timeout=default_timeout):
    """
    Attend que l'URL actuelle contienne une partie spécifique
    
    Args:
        driver: Instance du WebDriver
        expected_url_part: Partie de l'URL attendue
        timeout: Temps d'attente maximum en secondes
        
    Returns:
        bool: True si l'URL contient la partie attendue, False sinon
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: expected_url_part in d.current_url
        )
        return True
    except TimeoutException:
        print(f"L'URL ne contient pas '{expected_url_part}' après {timeout} secondes. URL actuelle : {driver.current_url}")
        return False
    

def fill_field(browser, locator, value):
    """
    Remplit un champ de formulaire avec une valeur donnée
    Args:
        browser: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        value: Valeur à entrer dans le champ
    """
    field = wait_for_element_visible(browser, locator)
    if field:
        field.send_keys(value)


def login(browser, username, password):
    """
    Effectue une connexion à l'application avec les identifiants fournis
    Args:
        browser: Instance du WebDriver
        username: Nom d'utilisateur pour la connexion
        password: Mot de passe pour la connexion
    """
    browser.get("https://www.saucedemo.com")
    fill_field(browser, ("id", "user-name"), username)
    fill_field(browser, ("id", "password"), password)
    click_element(browser, ("id", "login-button"))


def localiser_produit_par_nom(context, product_name):
    """
     Localise un produit dans le panier par son nom
     Args:
         context: Contexte de test Behave
         product_name: Nom du produit à localiser
    Returns:
         WebElement du produit trouvé ou None
    """
    xpath = f"//div[text()='{product_name}' and @data-test='inventory-item-name']//ancestor::div[@data-test='inventory-item']"
    product_element = wait_for_element_visible(context.browser, (By.XPATH, xpath))
    assert product_element is not None, f"Produit '{product_name}' non trouvé sur la page"
    return product_element

def localiser_cta_produit(context, product_name):
    """Localise le bouton d'ajout ou de suppression d'un produit dans le panier par son nom
    Args:
        context: Contexte de test Behave
        product_name: Nom du produit pour lequel localiser le bouton
    Returns:
        WebElement du bouton trouvé ou None
    """
    product_element = localiser_produit_par_nom(context, product_name)
    # Localiser le bouton à l'intérieur du produit
    xpath_button = ".//button[contains(@data-test, 'add-to-cart') or contains(@data-test, 'remove')]"
    try:
        button = product_element.find_element(By.XPATH, xpath_button)
    except NoSuchElementException:
        print(f"Le bouton d'ajout ou de suppression pour le produit '{product_name}' n'a pas été trouvé")
        return None
    return button

def click_bouton_link_panier(context):
    """Clique sur le lien du panier pour accéder à la page du panier
    Args:
        context: Contexte de test Behave
    """
    cart_link = wait_for_element_clickable(context.browser, InventoryPageLocators.SHOPPING_CART_LINK)
    assert cart_link is not None, "Le lien du panier n'a pas été trouvé"
    cart_link.click()