#!/usr/bin/env python3
"""
Script de test pour vérifier la création de liens entre tickets Jira.
Utilise les mêmes fonctions que le script principal.
"""

import os
import sys
import json
import urllib.request
import urllib.error

# Configuration Jira
JIRA_BASE = os.getenv("JIRA_BASE_URL", "https://aqaformation.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")

if not JIRA_EMAIL or not JIRA_TOKEN:
    print("❌ Variables d'environnement JIRA_EMAIL et JIRA_API_TOKEN requises")
    sys.exit(1)

# Headers communs
import base64
auth_str = f"{JIRA_EMAIL}:{JIRA_TOKEN}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {auth_b64}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

print(f"🔧 Test de création de lien Jira")
print(f"   Base URL: {JIRA_BASE}")
print(f"   Email: {JIRA_EMAIL}")
print()

# Test 1: Récupérer les types de liens disponibles
print("📋 Étape 1: Récupération des types de liens disponibles")
try:
    req = urllib.request.Request(
        f"{JIRA_BASE}/rest/api/3/issueLinkType",
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        link_types = json.loads(resp.read().decode("utf-8"))
        print(f"   ✅ Types de liens disponibles:")
        for lt in link_types.get("issueLinkTypes", []):
            print(f"      - {lt['name']} (inward: '{lt['inward']}', outward: '{lt['outward']}')")
except Exception as e:
    print(f"   ⚠️  Erreur: {e}")

print()

# Test 2: Créer un lien de test entre deux tickets
print("📋 Étape 2: Test de création de lien")
print("   Entrez la clé du ticket BUG (ex: BUG-95): ", end="")
bug_key = input().strip()
print("   Entrez la clé du ticket TEST CASE (ex: PSD-145): ", end="")
test_case_key = input().strip()

if not bug_key or not test_case_key:
    print("   ⚠️  Clés de tickets requises")
    sys.exit(1)

# Essayer différents types de liens
link_types_to_test = [
    "Relates",
    "Tests",
    "Blocks",
    "Cloners"
]

for link_type in link_types_to_test:
    print(f"\n   Test avec type '{link_type}'...")
    
    link_payload = json.dumps({
        "type": {"name": link_type},
        "inwardIssue": {"key": bug_key},
        "outwardIssue": {"key": test_case_key}
    }).encode("utf-8")
    
    try:
        link_req = urllib.request.Request(
            f"{JIRA_BASE}/rest/api/3/issueLink",
            data=link_payload,
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(link_req) as resp:
            print(f"      ✅ Lien créé avec succès! (HTTP {resp.status})")
            print(f"         {bug_key} ↔ {test_case_key}")
            break  # Succès, on sort de la boucle
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        print(f"      ❌ Erreur HTTP {e.code}")
        try:
            error_json = json.loads(error_body)
            if "errorMessages" in error_json:
                for msg in error_json["errorMessages"]:
                    print(f"         • {msg}")
            if "errors" in error_json:
                for field, msg in error_json["errors"].items():
                    print(f"         • {field}: {msg}")
        except:
            print(f"         Réponse brute: {error_body[:200]}")
    except Exception as e:
        print(f"      ⚠️  Erreur: {type(e).__name__} - {e}")

print("\n✅ Test terminé")
