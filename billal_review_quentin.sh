#!/bin/bash

# Configuration
BRANCH_NAME="quentin-automatisation"
VENV_DIR=".venv"

echo "🚀 Billal lance la revue de la branche : $BRANCH_NAME"

# 1. Activation de l'environnement virtuel
if [ -d "$VENV_DIR" ]; then
    source $VENV_DIR/bin/activate
    echo "✅ Environnement $VENV_DIR activé."
else
    echo "❌ Erreur : Dossier '$VENV_DIR' introuvable. Vérifie ton installation."
    exit 1
fi

# 2. Synchronisation forcée (Mode Lead : On écrase tout le superflu)
echo "🔄 Nettoyage et récupération forcée de origin/$BRANCH_NAME..."
git fetch origin
git checkout $BRANCH_NAME
git reset --hard origin/$BRANCH_NAME
echo "✅ Branche synchronisée (Code de Quentin à jour)."

# 3. Préparation des dossiers Allure
echo "🧹 Purge des anciens rapports..."
rm -rf allure-results/*
rm -rf allure-report/*
mkdir -p allure-results

# 4. Exécution des tests Behave
echo "🧪 Exécution des tests (Focus : Tri et Catalogue)..."
# On filtre sur les tags de Quentin pour un feedback rapide
behave -f allure_behave.formatter:AllureFormatter -o allure-results/ --tags=@sort,@tc-cat-34,@tc-cat-35

# 5. Génération et ouverture du rapport
if command -v allure &> /dev/null
then
    echo "📊 Génération du rapport Allure en cours..."
    allure generate allure-results/ -o allure-report/ --clean
    echo "🌐 Ouverture du rapport Billal vs Quentin..."
    allure open allure-report/
else
    echo "⚠️ Logiciel 'allure' absent du système."
    echo "💡 Les résultats JSON sont dans 'allure-results/'."
fi
