import os
import allure
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

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

def before_all(context):
    print("Début des tests")
    context.base_url = "https://www.saucedemo.com"

    # ✅ Détection automatique du mode Headless via la variable d'env du YAML
    context.headless = os.getenv("HEADLESS", "false").lower() == "true"

def before_scenario(context, scenario):
    step_logger.info(f"Début du scénario: {scenario.name}")
    if "web" in scenario.effective_tags:
        step_logger.info("Initialisation du navigateur Chrome")

        options = webdriver.ChromeOptions()

        # ✅ Mode Headless dynamique pour la CI
        if context.headless:
            step_logger.info("Mode HEADLESS activé (CI)")
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")

        # Désactive le gestionnaire de mots de passe
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        options.add_experimental_option("prefs", prefs)

        # ✅ Selenium 4 gère ChromeDriver automatiquement — plus besoin de ChromeDriverManager
        context.browser = webdriver.Chrome(options=options)

        if not context.headless:
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

            # ✅ Screenshot attaché directement au rapport Allure
            allure.attach(
                context.browser.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            # Sauvegarde également en fichier local (uploadé par la CI)
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
    print("Fin des tests")