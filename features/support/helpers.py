"""
Fonctions utilitaires pour les tests Selenium
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


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


def wait_for_element(driver, locator, timeout=10):
    """
    Attend qu'un élément soit présent dans le DOM
    
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


def wait_for_element_clickable(driver, locator, timeout=10):
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


def wait_for_element_visible(driver, locator, timeout=10):
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


def get_element_text(driver, locator, timeout=10):
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


def click_element(driver, locator, timeout=10):
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


def send_keys_to_element(driver, locator, text, timeout=10):
    """
    Envoie du texte à un élément input
    
    Args:
        driver: Instance du WebDriver
        locator: Tuple (By.METHOD, "selector")
        text: Texte à envoyer
        timeout: Temps d'attente maximum en secondes
        
    Returns:
        bool: True si l'envoi a réussi, False sinon
    """
    element = wait_for_element(driver, locator, timeout)
    if element:
        element.clear()
        element.send_keys(text)
        return True
    return False
