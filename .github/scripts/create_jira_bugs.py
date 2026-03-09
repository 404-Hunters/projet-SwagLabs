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
import urllib.parse
import urllib.error
import os
import mimetypes
import re
import time
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

headers_multipart = {
    "Authorization": f"Basic {credentials}",
    "X-Atlassian-Token": "no-check",
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


def adf_table_row(cells):
    """Crée une ligne de tableau ADF."""
    return {"type": "tableRow", "content": cells}


def adf_table_cell(text, is_header=False):
    """Crée une cellule de tableau ADF."""
    cell_type = "tableHeader" if is_header else "tableCell"
    return {
        "type": cell_type,
        "attrs": {},
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": str(text)}]}]
    }


def adf_info_table(data):
    """
    Crée un tableau à 2 colonnes (Champ | Valeur) pour afficher des informations.
    
    Args:
        data: Liste de tuples (champ, valeur)
        
    Returns:
        Dictionnaire ADF représentant un tableau
    """
    # Ligne d'en-tête avec les titres des colonnes
    header_row = adf_table_row([
        adf_table_cell("Champ", is_header=True),
        adf_table_cell("Valeur", is_header=True)
    ])
    
    # Lignes de données
    data_rows = [
        adf_table_row([
            adf_table_cell(champ),
            adf_table_cell(valeur)
        ])
        for champ, valeur in data
    ]
    
    return {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
        "content": [header_row] + data_rows
    }


def table_to_text(table_data):
    """
    Convertit un tableau Gherkin en texte formaté pour l'affichage dans un paragraph.
    
    Args:
        table_data: Liste de listes représentant les lignes du tableau
        
    Returns:
        Chaîne de texte formatée avec les données du tableau
    """
    if not table_data or not isinstance(table_data, list):
        return ""
    
    lines = []
    for row in table_data:
        if isinstance(row, list):
            # Convertir toutes les cellules en string et joindre avec " | "
            row_str = " | ".join(str(cell) for cell in row)
            lines.append(row_str)
    
    return "\n".join(lines) if lines else ""


def adf_data_table(table_data):
    """
    Crée un tableau ADF à partir des données d'une data table Gherkin.
    
    Args:
        table_data: Liste de listes représentant les lignes du tableau (avec header en première ligne)
        
    Returns:
        Dictionnaire ADF représentant un tableau, ou None si invalide
    """
    if not table_data or len(table_data) < 1:
        return None
    
    # Validation : vérifier que c'est bien une liste de listes
    if not isinstance(table_data, list):
        print(f"  ⚠️  table_data n'est pas une liste: {type(table_data)}")
        return None
    
    rows = []
    for i, row in enumerate(table_data):
        if not isinstance(row, list):
            print(f"  ⚠️  Ligne {i} n'est pas une liste: {type(row)}")
            continue
            
        is_header = (i == 0)  # Première ligne = header
        cells = [adf_table_cell(str(cell), is_header=is_header) for cell in row]
        rows.append(adf_table_row(cells))
    
    if not rows:
        return None
    
    return {
        "type": "table",
        "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
        "content": rows
    }


# ── Appels API Jira ─────────────────────────────────────────────────────────
def ticket_exists(bug_id):
    """
    Vérifie si un ticket de bug existe déjà dans Jira.
    
    Args:
        bug_id: L'identifiant du bug (ex: "BUG-CART-01-standard_user")
        
    Returns:
        La clé du ticket s'il existe, None sinon
    """
    # Utilisation du nouvel endpoint /search/jql (l'ancien /search a été supprimé)
    # Recherche avec 'text' qui fonctionne sur cette instance Jira
    jql = f'project = PSD AND issuetype = Bug AND text ~ "{bug_id}"'
    params = urllib.parse.urlencode({"jql": jql, "fields": "key,summary", "maxResults": 10})
    
    req = urllib.request.Request(
        f"{JIRA_BASE}/rest/api/3/search/jql?{params}",
        headers=headers,
        method="GET",
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.load(resp)
            issues = result.get("issues", [])
            if issues:
                # Vérifier que le bug_id est exactement dans le summary
                for issue in issues:
                    summary = issue['fields']['summary']
                    # Le summary contient : [BUG] BUG-CAT-36-locked_out_user
                    if bug_id in summary:
                        print(f"  ✅ Ticket existant trouvé : {issue['key']} - {summary}")
                        return issue["key"]
            print(f"  ℹ️  Aucun ticket existant pour : {bug_id}")
            return None
    except urllib.error.HTTPError as e:
        print(f"  ⚠️  Erreur HTTP {e.code} lors de la vérification : {e.reason}")
        return None
    except Exception as e:
        print(f"  ⚠️  Erreur lors de la vérification : {e}")
        return None


def upload_attachment(issue_key, file_path):
    """
    Upload une pièce jointe à un ticket Jira avec retry robuste.
    
    Args:
        issue_key: Clé du ticket Jira (ex: "PSD-123")
        file_path: Chemin du fichier à uploader
        
    Returns:
        L'ID de l'attachement uploadé, ou None en cas d'erreur
    """
    if not os.path.exists(file_path):
        print(f"  ⚠️  Fichier non trouvé : {file_path}")
        return None
    
    # Vérifier la taille du fichier
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    
    # Déterminer le type MIME
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"
    
    filename = os.path.basename(file_path)
    print(f"  📤 Upload en cours : {filename} ({file_size_mb:.2f} MB, {mime_type})")
    
    # Lire le fichier
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    # Préparer le multipart/form-data
    boundary = "----WebKitFormBoundary" + base64.b64encode(os.urandom(16)).decode()[:16]
    
    # Encoder le nom de fichier selon RFC 2231 pour gérer les caractères spéciaux
    filename_encoded = urllib.parse.quote(filename, safe='')
    
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"; filename*=UTF-8\'\'{filename_encoded}\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode('utf-8') + file_content + f"\r\n--{boundary}--\r\n".encode('utf-8')
    
    headers_upload = {
        "Authorization": f"Basic {credentials}",
        "X-Atlassian-Token": "no-check",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    
    # Timeout adaptatif : 30s de base + 10s par MB
    adaptive_timeout = max(30, int(30 + file_size_mb * 10))
    
    # Configuration du retry
    max_retries = 3
    retry_delay = 6  # secondes
    
    req = urllib.request.Request(
        f"{JIRA_BASE}/rest/api/3/issue/{issue_key}/attachments",
        data=body,
        headers=headers_upload,
        method="POST",
    )
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=adaptive_timeout) as resp:
                result = json.load(resp)
                if result:
                    attachment_id = result[0].get("id")
                    print(f"  📎 Screenshot uploadé : {filename} (ID: {attachment_id})")
                    return attachment_id
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            
            if e.code == 500:
                if attempt < max_retries - 1:
                    print(f"  ⚠️  Erreur HTTP 500 (tentative {attempt + 1}/{max_retries}) - retry dans {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"  ⚠️  Erreur HTTP 500 persistante après {max_retries} tentatives")
                    print(f"      Fichier : {filename} ({file_size_mb:.2f} MB)")
                    print(f"      Détails : {error_body[:200]}")
            elif e.code == 413:
                print(f"  ⚠️  Fichier trop volumineux ({file_size_mb:.2f} MB) - limite Jira dépassée")
                return None
            else:
                print(f"  ⚠️  Erreur HTTP {e.code} lors de l'upload : {e.reason}")
                print(f"      Détails : {error_body[:200]}")
            break
        except urllib.error.URLError as e:
            print(f"  ⚠️  Erreur réseau (tentative {attempt + 1}/{max_retries}) : {e.reason}")
            if attempt < max_retries - 1:
                print(f"      Nouvelle tentative dans {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            break
        except Exception as e:
            print(f"  ⚠️  Erreur lors de l'upload : {e}")
            break
    
    return None


def adf_media_image(attachment_id, filename):
    """
    Crée un élément média image ADF pour afficher une pièce jointe.
    
    Args:
        attachment_id: ID de l'attachement dans Jira
        filename: Nom du fichier
        
    Returns:
        Dictionnaire ADF pour afficher l'image
    """
    return {
        "type": "mediaSingle",
        "attrs": {"layout": "center"},
        "content": [
            {
                "type": "media",
                "attrs": {
                    "type": "file",
                    "id": attachment_id,
                    "collection": "",
                    "alt": filename,
                }
            }
        ]
    }


def create_ticket(summary, description_adf, epic_key=None):
    """
    Crée un ticket de bug dans Jira.
    
    Args:
        summary: Le titre du ticket
        description_adf: La description au format ADF
        epic_key: Clé de l'EPIC parent (ex: "PSD-95"), optionnel
        
    Returns:
        La clé du ticket créé (ex: "PSD-123")
    """
    fields = {
        "project": {"key": "PSD"},
        "issuetype": {"name": "Bug"},
        "summary": summary,
        "description": description_adf,
        "labels": ["Automatique"],
    }
    
    # Lier le bug à son EPIC parent si fourni
    if epic_key:
        fields["parent"] = {"key": epic_key}

    payload = json.dumps({"fields": fields}).encode("utf-8")
    
    # Debug: afficher le payload en cas d'erreur
    # print(f"DEBUG Payload: {json.dumps(description_adf, indent=2)}")
    
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
        # Debug: afficher la description ADF en cas d'erreur
        print(f"DEBUG Description ADF qui a échoué:")
        print(json.dumps(description_adf, indent=2))
        raise


def transition_to_bug(issue_key):
    """
    Tente de faire passer le ticket à l'état "BUG".
    
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
    
    bug_id = next(
        (t["id"] for t in transitions if t["name"].lower() == "bug"),
        None
    )
    if bug_id:
        payload = json.dumps({"transition": {"id": bug_id}}).encode("utf-8")
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
        with urllib.request.urlopen(link_req) as resp:
            print(f"  🔗 Lien créé : {bug_key} ↔ {test_case_key} (HTTP {resp.status})")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        print(f"  ⚠️  Erreur HTTP {e.code} lors de la création du lien vers {test_case_key}")
        print(f"      Détails : {error_body[:300]}")
    except Exception as e:
        print(f"  ⚠️  Erreur lors de la création du lien vers {test_case_key} : {type(e).__name__} - {e}")


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
    elif "check" in tc_lower:
        return "Commande"
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
    
    # Nettoyer le nom du scénario (supprimer les tags -- @X.X)
    scenario_clean = re.sub(r'\s*--\s*@[\d.]+\s*', '', scenario).strip()
    
    # ── Résultat attendu (utiliser l'étape qui a réellement échoué) ────────
    steps_data = r.get("steps", [])
    failed_step_name = step.get("step_name", "")
    
    # Chercher l'étape qui correspond au failed_step dans les steps
    expected_content = []
    if failed_step_name and steps_data:
        # Trouver l'étape échouée dans la liste
        failed_step_obj = None
        for s in steps_data:
            if isinstance(s, dict):
                step_text = s.get("text", "")
                # Comparer sans le préfixe (given/when/then)
                step_text_clean = re.sub(r'^(given|when|then)\s+', '', step_text, flags=re.IGNORECASE)
                if step_text_clean == failed_step_name:
                    failed_step_obj = s
                    break
        
        if failed_step_obj:
            expected_text = failed_step_name
            
            # Ajouter le tableau en texte brut si présent
            if failed_step_obj.get("table"):
                table_text = table_to_text(failed_step_obj["table"])
                if table_text:
                    expected_text += "\n" + table_text
            
            expected_content.append(adf_paragraph(adf_text(expected_text)))
    
    # S'assurer qu'on a toujours au moins un élément
    if not expected_content:
        expected_content.append(adf_paragraph(adf_text("Voir le scénario Gherkin")))
    
    # ── Résultat obtenu ─────────────────────────────────────────────────────
    obtained = step.get("error", "N/A")
    
    # ── Étapes de reproduction ──────────────────────────────────────────────
    if steps_data:
        step_items = []
        for s in steps_data:
            if isinstance(s, dict):
                step_text = s.get("text", "")
                
                # Ajouter le tableau en texte préformaté si présent
                if s.get("table"):
                    table_text = table_to_text(s["table"])
                    if table_text:
                        step_text += "\n" + table_text
                
                step_items.append({"type": "listItem", "content": [adf_paragraph(adf_text(step_text))]})
            else:
                # Rétro-compatibilité : si c'est une string simple
                step_items.append({"type": "listItem", "content": [adf_paragraph(adf_text(str(s)))]})
        
        steps_block = {
            "type": "orderedList",
            "content": step_items
        }
    else:
        steps_block = adf_paragraph(adf_text("Aucune étape disponible."))
    
    # ── Description ADF ─────────────────────────────────────────────────────
    return {
        "type": "doc", "version": 1,
        "content": [
            # ── Titre ───────────────────────────────────────────────────────
            adf_heading(f"ANOMALIE {bug_id} - Echec du scenario {scenario_clean}", 3),

            # ── Informations générales (tableau) ────────────────────────────
            adf_heading("Informations generales", 3),
            adf_info_table([
                ("ID", bug_id),
                ("Statut", "Ouvert"),
                ("Priorite", "Majeure"),
                ("Severite", "Haute"),
                ("Module", module),
                ("Environnement", "Test - Chrome - Ubuntu (CI)"),
                ("Rapporte par", actor),
                ("Date", run_date),
            ]),

            # ── Description ─────────────────────────────────────────────────
            adf_heading("Description", 3),
            adf_paragraph(adf_text(
                f"Echec automatique detecte sur le scenario '{scenario_clean}' "
                f"lors de l'execution avec le profil '{username}'."
            )),

            # ── Étapes de reproduction ──────────────────────────────────────
            adf_heading("Etapes de reproduction", 3),
            steps_block,

            # ── Résultat obtenu ─────────────────────────────────────────────
            adf_heading("Resultat obtenu", 3),
            adf_paragraph(adf_text(obtained)),

            # ── Résultat attendu ────────────────────────────────────────────
            adf_heading("Resultat attendu", 3),
        ] + expected_content + [

            # ── Impact ──────────────────────────────────────────────────────
            adf_heading("Impact", 3),
            adf_paragraph(adf_text(
                f"Le profil '{username}' ne peut pas effectuer cette action correctement. "
                f"Risque de regression fonctionnelle sur le module {module}."
            )),

            # ── Preuves ─────────────────────────────────────────────────────
            adf_heading("Preuves", 3),
            adf_paragraph(adf_text("Screenshot de l'erreur : voir piece jointe ci-dessous")),
            adf_paragraph(adf_text(f"Rapport Allure complet : {allure_url}")),

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
    
    # Track les liens déjà créés pour éviter les doublons
    created_links = set()
    
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
        tc_tag = next((t for t in tags if t.lower().startswith("tc-")), None)
        if tc_tag:
            tc_id = tc_tag.upper().replace("TC-", "")
            bug_id = f"BUG-{tc_id}-{username}"
        else:
            tc_id = "UNKNOWN"
            bug_id = f"BUG-UNKNOWN-{username}"

        # Extraire l'EPIC parent depuis les tags (format: @epic-PSD-95)
        epic_tag = next((t for t in tags if t.lower().startswith("epic-")), None)
        epic_key = epic_tag.replace("epic-", "").replace("EPIC-", "").upper() if epic_tag else None

        module = determine_module(tc_tag)
        summary = f"[BUG] {bug_id}"

        # ── Vérifier si le ticket existe déjà ───────────────────────────────
        existing_key = ticket_exists(bug_id)
        if existing_key:
            # Upload du screenshot même sur ticket existant (complète ou met à jour)
            if screenshot and os.path.exists(screenshot):
                upload_attachment(existing_key, screenshot)
            
            # Créer le lien vers le test case si absent
            test_case_key = next(
                (t.upper() for t in tags if t.upper().startswith("PSD-")),
                None
            )
            if test_case_key and test_case_key != existing_key:
                link_pair = (existing_key, test_case_key)
                if link_pair not in created_links:
                    link_to_test_case(existing_key, test_case_key, bug_id)
                    created_links.add(link_pair)
            
            print(f"⏭️  {existing_key} — {summary} (ticket déjà existant, ignoré)")
            continue

        # ── Construction de la description ──────────────────────────────────
        description_adf = build_bug_description(
            r, bug_id, scenario, module, username, step, screenshot
        )

        # ── Création du ticket ──────────────────────────────────────────────
        issue_key = create_ticket(summary, description_adf, epic_key)
        in_bug = transition_to_bug(issue_key)
        status = "✅ BUG" if in_bug else "⚠️  Backlog"
        print(f"{issue_key} [{status}] — {summary}")

        # ── Upload du screenshot ────────────────────────────────────────────
        if screenshot and os.path.exists(screenshot):
            upload_attachment(issue_key, screenshot)

        # ── Lien vers le ticket de cas de test ──────────────────────────────
        test_case_key = next(
            (t.upper() for t in tags if t.upper().startswith("PSD-")),
            None
        )
        if test_case_key and test_case_key != issue_key:
            link_pair = (issue_key, test_case_key)
            if link_pair not in created_links:
                link_to_test_case(issue_key, test_case_key, bug_id)
                created_links.add(link_pair)
        else:
            print(f"  ⚠️  Pas de tag PSD-XX dans les tags — lien ignore")


# ── Point d'entrée ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    process_failure_reports()
