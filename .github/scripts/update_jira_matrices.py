#!/usr/bin/env python3
"""
Script pour mettre à jour les matrices d'exécution des tests dans Jira.

Ce script génère et pousse des matrices au format ADF (Atlassian Document Format)
dans un champ personnalisé de chaque ticket de cas de test Jira.

La matrice affiche les résultats d'exécution (PASS/FAIL) pour chaque profil utilisateur
et chaque étape du scénario Gherkin.

Usage:
    python update_jira_matrices.py

Variables d'environnement requises:
    - JIRA_BASE_URL
    - JIRA_USER_EMAIL
    - JIRA_API_TOKEN
    - GITHUB_ACTOR (utilisateur GitHub)
"""

import glob
import json
import base64
import urllib.request
import os
from datetime import datetime, timezone
from collections import defaultdict


# ── Configuration ───────────────────────────────────────────────────────────
CUSTOM_FIELD = "customfield_10104"  # Champ personnalisé pour la matrice d'exécution
JIRA_BASE = os.environ.get("JIRA_BASE_URL", "")
JIRA_USER_EMAIL = os.environ.get("JIRA_USER_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")
ACTOR = os.environ.get("GITHUB_ACTOR", "unknown")
RUN_DATE = datetime.now(timezone.utc).strftime("%d/%m/%Y")

# Liste complète des profils utilisateurs à tester
ALL_USERS = [
    "standard_user",
    "problem_user",
    "locked_out_user",
    "visual_user",
    "performance_glitch_user",
    "error_user",
]

# ── Authentification Jira ───────────────────────────────────────────────────
credentials = base64.b64encode(
    f"{JIRA_USER_EMAIL}:{JIRA_API_TOKEN}".encode()
).decode()

headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json",
}


# ── Helpers ADF (Atlassian Document Format) ─────────────────────────────────
def adf_cell(text, is_header=False):
    """
    Crée une cellule de tableau ADF.
    
    Args:
        text: Le texte à afficher dans la cellule
        is_header: Si True, crée une cellule d'en-tête
        
    Returns:
        Dictionnaire représentant une cellule ADF
    """
    cell_type = "tableHeader" if is_header else "tableCell"
    return {
        "type": cell_type,
        "attrs": {},
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": str(text)}]}]
    }


def adf_row(cells):
    """
    Crée une ligne de tableau ADF.
    
    Args:
        cells: Liste de cellules ADF
        
    Returns:
        Dictionnaire représentant une ligne ADF
    """
    return {"type": "tableRow", "content": cells}

def format_step_text(step):
    """
    Formate le texte d'une étape de test.
    Si l'étape contient un tableau, ajoute les éléments séparés par des virgules.
    
    Args:
        step: String simple ou dict avec 'text' et optionnellement 'table'
        
    Returns:
        String formatée pour l'affichage
    """
    # Cas simple : step est déjà une string
    if isinstance(step, str):
        return step
    
    # Cas dict : extraire le texte et éventuellement le tableau
    if isinstance(step, dict):
        step_text = step.get("text", "")
        table_data = step.get("table")
        
        # Si un tableau est présent, ajouter les éléments séparés par des virgules
        if table_data and isinstance(table_data, list):
            # Aplatir toutes les lignes du tableau en une seule liste d'éléments
            all_items = []
            for row in table_data:
                if isinstance(row, list):
                    all_items.extend(str(cell) for cell in row)
            
            if all_items:
                step_text += " : " + ", ".join(all_items)
        
        return step_text
    
    # Fallback : convertir en string
    return str(step)

# ── API Jira ────────────────────────────────────────────────────────────────
def jira_put(path, payload):
    """
    Effectue une requête PUT sur l'API Jira.
    
    Args:
        path: Le chemin de l'endpoint API (ex: "/rest/api/3/issue/PSD-123")
        payload: Le payload JSON à envoyer
        
    Returns:
        Le code de statut HTTP de la réponse
    """
    req = urllib.request.Request(
        f"{JIRA_BASE}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="PUT",
    )
    with urllib.request.urlopen(req) as r:
        return r.status


# ── Chargement des résultats ────────────────────────────────────────────────
def load_test_results():
    """
    Charge tous les résultats de tests depuis les fichiers JSON.
    
    Returns:
        Un dictionnaire avec les résultats organisés par tag de cas de test,
        puis par nom d'utilisateur
    """
    results = defaultdict(dict)

    # Charger les résultats de succès
    for path in glob.glob("reports/results/*.json"):
        with open(path, encoding="utf-8") as f:
            r = json.load(f)
        
        # Rechercher le tag du cas de test (ex: "tc-cart-01" ou "TC-CART-01")
        for tag in r.get("tags", []):
            if tag.lower().startswith("tc-"):
                results[tag.lower()][r["username"]] = {
                    "steps": r.get("steps", []),
                    "status": r.get("status", "PASS"),
                    "tags": r.get("tags", []),
                    "failed_step": None,
                }
    
    # Charger les échecs pour identifier l'étape échouée
    for path in glob.glob("reports/failures/*.json"):
        with open(path, encoding="utf-8") as f:
            r = json.load(f)
        
        for tag in r.get("tags", []):
            if tag.lower().startswith("tc-"):
                username = r.get("username")
                if username in results[tag.lower()]:
                    results[tag.lower()][username]["failed_step"] = r.get("failed_step", {})

    return results


# ── Construction de la matrice ADF ──────────────────────────────────────────
def build_matrix_adf(tc_tag, user_data):
    """
    Construit la matrice d'exécution au format ADF.
    
    Args:
        tc_tag: Le tag du cas de test (ex: "tc-cart-01")
        user_data: Dictionnaire des résultats par utilisateur
        
    Returns:
        Dictionnaire ADF représentant la matrice complète
    """
    # Récupérer les étapes du scénario (identiques pour tous les utilisateurs)
    first_result = next(iter(user_data.values()))
    steps = first_result["steps"]

    # ── Ligne d'en-tête ─────────────────────────────────────────────────────
    header_row = adf_row(
        [adf_cell("Étapes du Test (Gherkin)", True)]
        + [adf_cell(u, True) for u in ALL_USERS]
    )

    # ── Lignes des étapes ───────────────────────────────────────────────────
    step_rows = []
    for i, step in enumerate(steps, 1):
        # Formater l'étape (gère les tableaux s'ils sont présents)
        step_text = format_step_text(step)
        cells = [adf_cell(f"{i}. {step_text}")]
        
        for u in ALL_USERS:
            if u not in user_data:
                cells.append(adf_cell("-"))
            elif user_data[u]["status"] == "PASS":
                cells.append(adf_cell("✅"))
            else:
                # Test échoué : identifier l'étape qui a échoué
                failed_step_info = user_data[u].get("failed_step", {})
                failed_step_name = failed_step_info.get("step_name", "") if failed_step_info else ""
                
                # Debug: afficher l'info de l'étape échouée
                if i == 1:  # Seulement pour la première ligne pour éviter le spam
                    print(f"  [DEBUG] {tc_tag} - {u}: failed_step_name='{failed_step_name}'")
                
                # Extraire le nom de l'étape courante (sans le préfixe given/when/then)
                import re
                current_step_clean = re.sub(r'^(given|when|then)\s+', '', step_text, flags=re.IGNORECASE)
                
                # Trouver l'index de l'étape échouée
                failed_step_index = -1
                if failed_step_name:
                    # Normaliser le nom de l'étape échouée (remplacer les noms de produits variables)
                    failed_normalized = re.sub(r'"[^"]*"', '"{PRODUIT}"', failed_step_name)
                    
                    for idx, s in enumerate(steps):
                        s_text = format_step_text(s)
                        s_clean = re.sub(r'^(given|when|then)\s+', '', s_text, flags=re.IGNORECASE)
                        s_normalized = re.sub(r'"[^"]*"', '"{PRODUIT}"', s_clean)
                        
                        # Comparaison avec normalisation
                        if failed_normalized == s_normalized or failed_step_name in s_clean or s_clean == failed_step_name:
                            failed_step_index = idx
                            if i == 1:  # Log seulement une fois
                                print(f"      → Étape échouée trouvée à l'index {idx} (étape #{idx+1})")
                            break
                
                if failed_step_index == -1:
                    if i == 1:  # Log seulement une fois
                        print(f"      ⚠️  AUCUN MATCH trouvé - toutes les étapes seront marquées ❌")
                    # Pas d'info sur l'étape échouée, marquer toutes en échec (fallback)
                    cells.append(adf_cell("❌"))
                elif i - 1 < failed_step_index:
                    # Étape avant l'échec : passée avec succès
                    cells.append(adf_cell("✅"))
                elif i - 1 == failed_step_index:
                    # C'est l'étape qui a échoué
                    cells.append(adf_cell("❌"))
                else:
                    # Étape après l'échec : non exécutée
                    cells.append(adf_cell("⊘"))
        
        step_rows.append(adf_row(cells))

    # ── Ligne de résultat final ─────────────────────────────────────────────
    tc_id = tc_tag.upper().replace("TC-", "")
    final_cells = [adf_cell("RÉSULTAT FINAL")]
    for u in ALL_USERS:
        if u not in user_data:
            final_cells.append(adf_cell("-"))
        elif user_data[u]["status"] == "PASS":
            final_cells.append(adf_cell("✅ PASS"))
        else:
            final_cells.append(adf_cell(f"❌ BUG-{tc_id}-{u}"))
    final_row_adf = adf_row(final_cells)

    # ── Document ADF complet ────────────────────────────────────────────────
    adf_value = {
        "type": "doc", "version": 1,
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": f"Date de campagne : {RUN_DATE}"}]},
            {
                "type": "table",
                "attrs": {"isNumberColumnEnabled": False, "layout": "full-width"},
                "content": [header_row] + step_rows + [final_row_adf]
            },
            {"type": "paragraph", "content": [{"type": "text", "text": f"Exécuté par : {ACTOR}"}]},
        ]
    }

    return adf_value


# ── Mise à jour des tickets Jira ────────────────────────────────────────────
def update_jira_matrices():
    """
    Met à jour les matrices d'exécution sur tous les tickets de cas de test Jira.
    """
    # Charger tous les résultats
    results = load_test_results()

    if not results:
        print("Aucun résultat trouvé dans reports/results/ — job ignoré")
        return

    print(f"Traitement de {len(results)} cas de test...")

    # Pour chaque cas de test, construire et pousser la matrice
    for tc_tag, user_data in sorted(results.items()):
        
        # Récupérer la clé du ticket Jira depuis les tags
        first_result = next(iter(user_data.values()))
        issue_key = next(
            (t for t in first_result.get("tags", []) if t.upper().startswith("PSD-")),
            None
        )
        
        if not issue_key:
            print(f"⚠️  Pas de tag PSD-XX trouvé pour {tc_tag} — ticket ignoré")
            continue
        
        issue_key = issue_key.upper()

        # Construire la matrice ADF
        adf_value = build_matrix_adf(tc_tag, user_data)

        # Mettre à jour le ticket Jira
        status = jira_put(
            f"/rest/api/3/issue/{issue_key}",
            {"fields": {CUSTOM_FIELD: adf_value}}
        )
        
        status_icon = "✅" if status == 204 else "❌"
        print(f"{status_icon} {issue_key} ({tc_tag}) — matrice mise à jour (HTTP {status})")


# ── Point d'entrée ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    update_jira_matrices()
