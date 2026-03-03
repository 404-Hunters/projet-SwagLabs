#!/bin/bash

# Configuration
BRANCH_NAME="quentin-automatisation"
VENV_DIR=".venv"
PORT=8080

echo "🚀 Billal lance la revue intégrale (TOUS les TC) de la branche : $BRANCH_NAME"

# 1. Activation de l'environnement virtuel
if [ -d "$VENV_DIR" ]; then
    source $VENV_DIR/bin/activate
    echo "✅ Environnement $VENV_DIR activé."
else
    echo "❌ Erreur : Dossier '$VENV_DIR' introuvable."
    exit 1
fi

# 2. Synchronisation forcée
echo "🔄 Nettoyage et récupération forcée de origin/$BRANCH_NAME..."
git fetch origin
git checkout $BRANCH_NAME
git reset --hard origin/$BRANCH_NAME

# 3. Préparation des dossiers Allure
rm -rf allure-results/*
rm -rf allure-report/*
mkdir -p allure-results

# 4. Exécution de TOUS les tests Behave
echo "🧪 Lancement de la suite complète de tests (All TC)..."
# Suppression du filtre --tags pour tout exécuter
behave -f allure_behave.formatter:AllureFormatter -o allure-results/

# 5. Génération du rapport Allure
if command -v allure &> /dev/null
then
    echo "📊 Génération du rapport Allure..."
    allure generate allure-results/ -o allure-report/ --clean
    
    echo "🌐 Rapport prêt sur http://localhost:$PORT"
    echo "💡 (Appuie sur CTRL+C pour arrêter le serveur une fois la revue finie)"
    
    # Serveur Python de secours pour éviter l'erreur Java/Snap
    python3 -m http.server $PORT --directory allure-report/
else
    echo "❌ Allure n'est pas installé."
fi