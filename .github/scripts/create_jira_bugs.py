#!/usr/bin/env python3
"""
Script pour créer automatiquement des tickets de bug Jira
à partir des rapports JSON d'échecs de tests Behave.

Usage:
    python create_jira_bugs.py

Variables d'environnement requises:
    - JIRA_BASE_URL
    - JIRA_USER_EMAIL
    - JIRA_API_TOKEN
    - GITHUB_REF_NAME (branche)
    - GITHUB_SHA (commit)
    - GITHUB_ACTOR (utilisateur)
    - GITHUB_REPOSITORY_OWNER
    - GITHUB_REPOSITORY (format: owner/repo)
"""

import glob
import json
import base64
import urllib.request
import urllib.error
import os
from datetime import datetime, timezone


# ── Configuration ───────────────────────────────────────────────────────────
JIRA_BASE = os.environ.get("JIRA_BASE_URL", "")
JIRA_USER_EMAIL = os.environ.get("JIRA_USER_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")

branch = os.environ.get("GITHUB_REF_NAME", "unknown")
commit = os.environ.get("GITHUB_SHA", "unknown")
actor = os.environ.get("GITHUB_ACTOR", "unknown")
repo_owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "")
repo_name = os.environ.get("GITHUB_REPOSITORY", "").split("/")[-1] if os.environ.get("GITHUB_REPOSITORY") else ""

allure_url = f"https://{repo_owner}.github.io/{repo_name}/" if repo_owner and repo_name else "N/A"

# ── Authentification Jira ───────────────────────────────────────────────────
credentials = base64.b64encode(
    f"{JIRA_USER_EMAIL}:{JIRA_API_TOKEN}".encode()
).decode()

headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json",
}


# ── Helpers ADF (Atlassian Document Format) ─────────────────────────────────
def adf_text(text):
    """Crée un nœud texte ADF."""
    return {"type": "text", "text": str(text)}


def adf_paragraph(*texts):
    """Crée un paragraphe ADF."""
    return {"type": "paragraph", "content": list(texts)}


def adf_code_block(code):
    """Crée un bloc de code ADF."""
    return {
        "type": "codeBlock",
        "attrs": {"language": "text"},
        "content": [adf_text(code)]
    }


def adf_heading(text, level=3):
    """Crée un titre ADF."""
    return {
        "type": "heading",
        "attrs": {"level": level},
        "content": [adf_text(text)]
    }


def adf_bullet_list(items):
    """Crée une liste à puces ADF."""
    return {
        "type": "bulletList",
        "content": [
            {"type": "listItem", "content": [adf_paragraph(adf_text(item))]}
            for item in items
        ]
    }


# ── Appels API Jira ─────────────────────────────────────────────────────────
def create_ticket(summary, description_adf):
    """
    Crée un ticket de bug dans Jira.
    
    Args:
        summary: Le titre du ticket
        description_adf: La description au format ADF
        
    Returns:
        La clé du ticket créé (ex: "PSD-123")
    """
    fields = {
        "project": {"key": "PSD"},
        "issuetype": {"name": "Bug"},
        "summary": summary,
        "description": description_adf,
    }

    payload = json.dumps({"fields": fields}).encode("utf-8")
    req = urllib.request.Request(
        f"{JIRA_BASE}/rest/api/3/issue",
        data=payload,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp).get("key")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP {e.code} — Reponse Jira : {error_body}")
        raise


def transition_to_todo(issue_key):
    """
    Tente de faire passer le ticket à l'état "To Do" / "À faire".
    
    Args:
        issue_key: La clé du ticket Jira
        
    Returns:
        True si la transition a réussi, False sinon
    """
    req = urllib.request.Request(
        f"{JIRA_BASE}/rest/api/3/issue/{issue_key}/transitions",
        headers=headers,
    )
    with urllib.request.urlopen(req) as resp:
        transitions = json.load(resp)["transitions"]
    
    todo_id = next(
        (t["id"] for t in transitions if t["name"].lower() in ("to do", "à faire")),
        None
    )
    if todo_id:
        payload = json.dumps({"transition": {"id": todo_id}}).encode("utf-8")
        req = urllib.request.Request(
            f"{JIRA_BASE}/rest/api/3/issue/{issue_key}/transitions",
            data=payload,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req):
            return True
    return False


def link_to_test_case(bug_key, test_case_key, bug_id):
    """
    Crée un lien entre le ticket de bug et le ticket de cas de test.
    
    Args:
        bug_key: Clé du ticket de bug
        test_case_key: Clé du ticket de cas de test
        bug_id: Identifiant court du bug (ex: "BUG-CART-01-standard_user")
    """
    link_payload = json.dumps({
        "type": {"name": "Relates"},
        "inwardIssue": {"key": bug_key},
        "outwardIssue": {"key": test_case_key},
        "comment": {
            "body": {
                "type": "doc", "version": 1,
                "content": [adf_paragraph(
                    adf_text(f"Bug detecte automatiquement par la CI — {bug_id}")
                )]
            }
        }
    }).encode("utf-8")
    
    link_req = urllib.request.Request(
        f"{JIRA_BASE}/rest/api/3/issueLink",
        data=link_payload,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(link_req):
            print(f"  🔗 Lie a {test_case_key} (elements associes)")
    except Exception as e:
        print(f"  ⚠️  Lien echoue vers {test_case_key} : {e}")


def determine_module(tc_tag):
    """Détermine le module à partir du tag de cas de test."""
    if not tc_tag:
        return "Inconnu"
    
    tc_lower = tc_tag.lower()
    if "cat" in tc_lower:
        return "Catalogue"
    elif "auth" in tc_lower:
        return "Authentification"
    elif "cart" in tc_lower:
        return "Panier"
    elif "order" in tc_lower:
        return "Commande"
    return "Inconnu"


def build_bug_description(r, bug_id, scenario, module, username, step, screenshot):
    """
    Construit la description ADF du ticket de bug.
    
    Args:
        r: Données JSON du rapport d'échec
        bug_id: Identifiant du bug
        scenario: Nom du scénario
        module: Module concerné
        username: Profil utilisateur
        step: Dictionnaire de l'étape en échec
        screenshot: Chemin du screenshot
        
    Returns:
        Dictionnaire ADF pour la description
    """
    run_date = datetime.now(timezone.utc).strftime("%d/%m/%Y")
    
    # ── Résultat attendu ────────────────────────────────────────────────────
    then_steps = [s for s in r.get("steps", []) if s.startswith("then")]
    expected = then_steps[-1].replace("then ", "") if then_steps else "Voir le scénario Gherkin"
    
    # ── Résultat obtenu ─────────────────────────────────────────────────────
    obtained = step.get("error", "N/A")
    
    # ── Étapes de reproduction ──────────────────────────────────────────────
    steps_list = r.get("steps", [])
    steps_block = (
        {
            "type": "orderedList",
            "content": [
                {"type": "listItem", "content": [adf_paragraph(adf_text(s))]}
                for s in steps_list
            ]
        }
        if steps_list
        else adf_paragraph(adf_text("Aucune étape disponible."))
    )
    
    # ── Description ADF ─────────────────────────────────────────────────────
    return {
        "type": "doc", "version": 1,
        "content": [
            # ── Titre ───────────────────────────────────────────────────────
            adf_heading(f"ANOMALIE {bug_id} - Echec du scenario {scenario}", 3),

            # ── Informations générales ──────────────────────────────────────
            adf_heading("Informations generales", 3),
            {"type": "paragraph", "content": [{"type": "text", "text": "ID : ", "marks": [{"type": "strong"}]}, {"type": "text", "text": bug_id}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "Statut : ", "marks": [{"type": "strong"}]}, {"type": "text", "text": "Ouvert"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "Priorite : ", "marks": [{"type": "strong"}]}, {"type": "text", "text": "Majeure"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "Severite : ", "marks": [{"type": "strong"}]}, {"type": "text", "text": "Haute"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "Module : ", "marks": [{"type": "strong"}]}, {"type": "text", "text": module}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "Environnement : ", "marks": [{"type": "strong"}]}, {"type": "text", "text": "Test - Chrome - Ubuntu (CI)"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "Rapporte par : ", "marks": [{"type": "strong"}]}, {"type": "text", "text": actor}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "Date : ", "marks": [{"type": "strong"}]}, {"type": "text", "text": run_date}]},

            # ── Description ─────────────────────────────────────────────────
            adf_heading("Description", 3),
            adf_paragraph(adf_text(
                f"Echec automatique detecte sur le scenario '{scenario}' "
                f"lors de l'execution avec le profil '{username}'."
            )),

            # ── Étapes de reproduction ──────────────────────────────────────
            adf_heading("Etapes de reproduction", 3),
            steps_block,

            # ── Résultat obtenu ─────────────────────────────────────────────
            adf_heading("Resultat obtenu", 3),
            adf_code_block(obtained),

            # ── Résultat attendu ────────────────────────────────────────────
            adf_heading("Resultat attendu", 3),
            adf_paragraph(adf_text(expected)),

            # ── Impact ──────────────────────────────────────────────────────
            adf_heading("Impact", 3),
            adf_paragraph(adf_text(
                f"Le profil '{username}' ne peut pas effectuer cette action correctement. "
                f"Risque de regression fonctionnelle sur le module {module}."
            )),

            # ── Preuves ─────────────────────────────────────────────────────
            adf_heading("Preuves", 3),
            adf_bullet_list([
                f"Screenshot : {screenshot} (voir artefacts du run GitHub Actions)",
                f"Rapport Allure : {allure_url}",
            ]),

            # ── Informations techniques ─────────────────────────────────────
            adf_heading("Informations techniques", 3),
            adf_code_block(
                f"Etape en echec : {step.get('step_type', '')} {step.get('step_name', '')}\n"
                f"Erreur         : {obtained}\n"
                f"Tags           : {', '.join(r.get('tags', []))}\n"
                f"Workflow       : GitHub Actions CI"
            ),
        ]
    }


def process_failure_reports():
    """
    Traite tous les rapports JSON d'échecs et crée un ticket Jira pour chacun.
    """
    failure_files = sorted(glob.glob("reports/failures/*.json"))
    
    if not failure_files:
        print("Aucun rapport d'échec trouvé dans reports/failures/")
        return
    
    print(f"Traitement de {len(failure_files)} rapport(s) d'échec...")
    
    for path in failure_files:
        with open(path, encoding="utf-8") as f:
            r = json.load(f)

        # ── Extraction des données ──────────────────────────────────────────
        username = r.get("username", "inconnu")
        scenario = r.get("scenario", "")
        tags = r.get("tags", [])
        step = r.get("failed_step") or {}
        screenshot = r.get("screenshot_path", "")

        # ── Identifiants ────────────────────────────────────────────────────
        tc_tag = next((t for t in tags if t.startswith("tc-")), None)
        if tc_tag:
            tc_id = tc_tag.upper().replace("TC-", "")
            bug_id = f"BUG-{tc_id}-{username}"
        else:
            tc_id = "UNKNOWN"
            bug_id = f"BUG-UNKNOWN-{username}"

        module = determine_module(tc_tag)
        summary = f"[BUG] {bug_id}"

        # ── Construction de la description ──────────────────────────────────
        description_adf = build_bug_description(
            r, bug_id, scenario, module, username, step, screenshot
        )

        # ── Création du ticket ──────────────────────────────────────────────
        issue_key = create_ticket(summary, description_adf)
        in_todo = transition_to_todo(issue_key)
        status = "✅ To Do" if in_todo else "⚠️  Backlog"
        print(f"{issue_key} [{status}] — {summary}")

        # ── Lien vers le ticket de cas de test ──────────────────────────────
        test_case_key = next(
            (t.upper() for t in tags if t.upper().startswith("PSD-")),
            None
        )
        if test_case_key and test_case_key != issue_key:
            link_to_test_case(issue_key, test_case_key, bug_id)
        else:
            print(f"  ⚠️  Pas de tag PSD-XX dans les tags — lien ignore")


# ── Point d'entrée ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    process_failure_reports()
