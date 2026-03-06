import os
import re
import json
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

step_logger = logging.getLogger('steps')


def before_all(context):
    print("Début des tests")
    context.base_url = "https://www.saucedemo.com"
    context.headless  = os.getenv("HEADLESS", "false").lower() == "true"

    # Dossier qui contiendra un fichier JSON par scénario échoué
    # Le workflow CI lira ces fichiers pour créer les tickets Jira
    os.makedirs("reports/failures", exist_ok=True)


def before_scenario(context, scenario):
    step_logger.info(f"Début du scénario: {scenario.name}")

    # Réinitialise le step en échec à chaque scénario
    context.failed_step = None

    if "web" in scenario.effective_tags:
        step_logger.info("Initialisation du navigateur Chrome")

        options = webdriver.ChromeOptions()

        if context.headless:
            step_logger.info("Mode HEADLESS activé (CI)")
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        options.add_experimental_option("prefs", prefs)

        context.browser = webdriver.Chrome(options=options)

        if not context.headless:
            context.browser.maximize_window()

        step_logger.info("Navigateur Chrome initialisé avec succès")
        context.wait = WebDriverWait(context.browser, 10)


def before_step(context, step):
    step_logger.info(f"Exécution du step: {step.step_type} {step.name}")


def after_step(context, step):
    if step.status == "passed":
        step_logger.info(f"✓ Step réussi: {step.step_type} {step.name}")

    elif step.status == "failed":
        step_logger.error(f"✗ Step échoué: {step.step_type} {step.name}")

        # ── Capture du step en échec ──────────────────────────────────────
        # Stocké dans context pour être utilisé dans after_scenario
        error_message = ""
        if step.exception:
            error_message = str(step.exception)

        context.failed_step = {
            "step_type": step.step_type,   # given / when / then
            "step_name": step.name,
            "error":     error_message,
        }

    else:
        step_logger.warning(f"? Step status: {step.status} - {step.step_type} {step.name}")


def after_scenario(context, scenario):
    if hasattr(context, "browser"):

        if scenario.status == "failed":
            step_logger.error(f"Scénario échoué: {scenario.name}")

            # ── Screenshot ────────────────────────────────────────────────
            allure.attach(
                context.browser.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            os.makedirs("screenshots", exist_ok=True)
            # Supprime tous les caractères interdits par NTFS / GitHub Actions
            # (: " < > | * ? @ parenthèses et caractères non-ASCII)
            safe_name = scenario.name
            safe_name = safe_name.replace(" ", "_")
            safe_name = re.sub(r'[:"<>|*?@\(\)\r\n/]', "", safe_name)
            safe_name = re.sub(r'[^\x00-\x7F]', "", safe_name)  # retire accents/émojis
            safe_name = re.sub(r'_+', "_", safe_name).strip("_")  # dédoublonne les _
            screenshot_path = f"screenshots/{safe_name}.png"
            context.browser.save_screenshot(screenshot_path)
            step_logger.info(f"Screenshot sauvegardé : {screenshot_path}")

            # ── Rapport JSON pour le workflow CI / Jira ───────────────────
            # Extrait le username depuis le nom du scénario (suffixe "— <username>")
            # Exemple : "TC-CAT-36 - Tri par nom — problem_user"
            username = "inconnu"
            if " — " in scenario.name:
                username = scenario.name.split(" — ")[-1].strip()

            # Extrait les tags du scénario (ex: ["tc-cat-36", "web", "sort"])
            tags = list(scenario.effective_tags)

            failure_report = {
                "scenario":        scenario.name,
                "username":        username,
                "tags":            tags,
                "feature":         scenario.feature.filename,
                "failed_step":     context.failed_step,
                "screenshot_path": screenshot_path,
            }

            # Un fichier par scénario échoué → un ticket Jira par échec
            report_path = f"reports/failures/{safe_name}.json"
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(failure_report, f, ensure_ascii=False, indent=2)

            step_logger.info(f"Rapport d'échec écrit : {report_path}")

        else:
            step_logger.info(f"Scénario réussi: {scenario.name}")

        step_logger.info("Fermeture du navigateur")
        context.browser.quit()


def after_all(context):
    print("Fin des tests")