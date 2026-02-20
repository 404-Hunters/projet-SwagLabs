import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


import logging
import colorlog

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

def before_scenario(context, scenario):
    if "web" in scenario.effective_tags:
        service = Service(ChromeDriverManager().install())
        context.browser = webdriver.Chrome(service=service)
        context.browser.implicitly_wait(10)
        context.browser.maximize_window()

        # Ajouter le WebDriverWait réutilisable
        context.wait = WebDriverWait(context.browser, 10)

def after_scenario(context, scenario):
    if hasattr(context, "browser"):
        if scenario.status == "failed":
            os.makedirs("screenshots", exist_ok=True)
            name = scenario.name.replace(" ", "_")
            context.browser.save_screenshot(
                f"screenshots/{name}.png"
            )
        context.browser.quit()

def after_all(context):
    # Nettoyage global si nécessaire
    print("Fin des tests")