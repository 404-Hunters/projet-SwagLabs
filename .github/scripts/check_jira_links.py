#!/usr/bin/env python3
"""
Script pour vérifier les liens existants sur un ticket Jira.
"""

import os
import sys
import json
import urllib.request
import base64

# Configuration
JIRA_BASE = os.getenv("JIRA_BASE_URL", "https://aqaformation.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")

if not JIRA_EMAIL or not JIRA_TOKEN:
    print("❌ Variables JIRA_EMAIL et JIRA_API_TOKEN requises")
    sys.exit(1)

auth_str = f"{JIRA_EMAIL}:{JIRA_TOKEN}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {auth_b64}",
    "Accept": "application/json",
}

def get_issue_links(issue_key):
    """Récupère tous les liens d'un ticket."""
    try:
        req = urllib.request.Request(
            f"{JIRA_BASE}/rest/api/3/issue/{issue_key}?fields=issuelinks",
            headers=headers
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("fields", {}).get("issuelinks", [])
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return []

# Tickets à vérifier (bugs récents)
test_tickets = [
    "PSD-312",  # BUG-CART-02-problem_user
    "PSD-313",  # BUG-CART-03-problem_user
    "PSD-315",  # BUG-CHECK-08-problem_user
    "PSD-282",  # BUG-CAT-36-locked_out_user
]

print("🔍 Vérification des liens Jira...\n")

for ticket in test_tickets:
    print(f"📋 {ticket}:")
    links = get_issue_links(ticket)
    
    if not links:
        print("   ⚠️  Aucun lien trouvé")
    else:
        for link in links:
            link_type = link.get("type", {}).get("name", "Unknown")
            
            # Lien sortant (outward)
            if "outwardIssue" in link:
                target = link["outwardIssue"]["key"]
                relation = link["type"].get("outward", "relates to")
                print(f"   → {relation} {target}")
            
            # Lien entrant (inward)
            if "inwardIssue" in link:
                source = link["inwardIssue"]["key"]
                relation = link["type"].get("inward", "relates to")
                print(f"   ← {relation} {source}")
    
    print()

print("✅ Vérification terminée")
