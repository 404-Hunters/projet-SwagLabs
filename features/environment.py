import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


import logging
import colorlog

# Configuration du logging coloré
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s%(reset)s:%(name)s: %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
))

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Logger pour les steps
step_logger = logging.getLogger('steps')

def before_scenario(context, scenario):
    step_logger.info(f"Début du scénario: {scenario.name}")
    if "web" in scenario.effective_tags:
        step_logger.info("Initialisation du navigateur Chrome")
        service = Service(ChromeDriverManager().install())
        context.browser = webdriver.Chrome(service=service)
        context.browser.implicitly_wait(10)
        context.browser.maximize_window()
        step_logger.info("Navigateur Chrome initialisé avec succès")

        # Ajouter le WebDriverWait réutilisable
        context.wait = WebDriverWait(context.browser, 10)

def before_step(context, step):
    step_logger.info(f"Exécution du step: {step.step_type} {step.name}")

def after_step(context, step):
    if step.status == "passed":
        step_logger.info(f"✓ Step réussi: {step.step_type} {step.name}")
    elif step.status == "failed":
        step_logger.error(f"✗ Step échoué: {step.step_type} {step.name}")
    else:
        step_logger.warning(f"? Step status: {step.status} - {step.step_type} {step.name}")

def after_scenario(context, scenario):
    if hasattr(context, "browser"):
        if scenario.status == "failed":
            step_logger.error(f"Scénario échoué: {scenario.name}")
            os.makedirs("screenshots", exist_ok=True)
            name = scenario.name.replace(" ", "_")
            screenshot_path = f"screenshots/{name}.png"
            context.browser.save_screenshot(screenshot_path)
            step_logger.info(f"Screenshot sauvegardé: {screenshot_path}")
        else:
            step_logger.info(f"Scénario réussi: {scenario.name}")
        
        step_logger.info("Fermeture du navigateur")
        context.browser.quit()

def after_all(context):
    # Nettoyage global si nécessaire
    print("Fin des tests")