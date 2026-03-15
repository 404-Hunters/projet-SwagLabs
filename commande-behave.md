# Commandes Behave - Guide Complet

## Commandes de base

### Lancer tous les tests

```bash
behave
```

### Lancer avec affichage détaillé (verbose)

```bash
behave -v
behave --verbose
```

### Lancer un fichier feature spécifique

```bash
behave features/login.feature
behave features/nom_du_fichier.feature
```

### Lancer un scénario spécifique (par numéro de ligne)

```bash
behave features/login.feature:4
behave features/login.feature:10
```

### Lancer plusieurs fichiers

```bash
behave features/login.feature features/register.feature
```

---

## Filtrage par tags

### Lancer les tests avec un tag spécifique

```bash
behave --tags=@web
behave --tags=@smoke
behave --tags=@login
```

### Exclure un tag

```bash
behave --tags=~@wip
behave --tags=~@slow
```

### Combiner plusieurs tags (ET logique)

```bash
behave --tags=@web --tags=@smoke
behave --tags="@web and @smoke"
```

### Combiner plusieurs tags (OU logique)

```bash
behave --tags="@smoke or @regression"
```

### Tags complexes

```bash
behave --tags="@web and not @wip"
behave --tags="(@smoke or @regression) and @web"
```

---

## Formats de sortie

### Format par défaut (pretty)

```bash
behave --format=pretty
```

### Format concis

```bash
behave --format=progress
```

### Format JSON (pour rapports)

```bash
behave --format=json -o report.json
behave --format=json.pretty -o report.json
```

### Format JUnit XML

```bash
behave --junit
behave --junit --junit-directory=reports/
```

### Format HTML (nécessite behave-html-formatter)

```bash
pip install behave-html-formatter
behave -f html -o report.html
```

### Plusieurs formats en même temps

```bash
behave --format=pretty --format=json -o report.json
```

---

## Options d'affichage

### Afficher les steps non implémentés (snippets)

```bash
behave --snippets
```

### Ne pas afficher les snippets

```bash
behave --no-snippets
```

### Afficher le code source

```bash
behave --show-source
```

### Afficher les timings (durée d'exécution)

```bash
behave --show-timings
```

### Afficher uniquement le résumé

```bash
behave --no-summary
```

### Mode silencieux (quiet)

```bash
behave --quiet
behave -q
```

---

## Mode dry-run (simulation)

### Vérifier la syntaxe sans exécuter

```bash
behave --dry-run
behave -d
```

---

## Gestion des échecs

### Arrêter au premier échec

```bash
behave --stop
behave -x
```

### Continuer malgré les échecs

```bash
behave --no-stop
```

### Relancer uniquement les scénarios qui ont échoué

```bash
behave @rerun.txt
```

(Nécessite d'avoir d'abord généré le fichier avec `--format=rerun`)

---

## Capture et logging

### Désactiver la capture de stdout

```bash
behave --no-capture
```

### Désactiver la capture de stderr

```bash
behave --no-capture-stderr
```

### Activer les logs

```bash
behave --logging-level=INFO
behave --logging-level=DEBUG
behave --logging-level=WARNING
```

### Sauvegarder les logs dans un fichier

```bash
behave --logging-level=DEBUG --logcapture
```

---

## Exécution parallèle

### Avec behave-parallel (nécessite installation)

```bash
pip install behave-parallel
behave --processes 4
behave --parallel-processes 4
```

---

## Configuration et environnement

### Utiliser un fichier de configuration spécifique

```bash
behave -c behave.ini
behave --config=my_config.ini
```

### Passer des variables d'environnement

```bash
behave -D browser=firefox
behave -D env=staging
behave --define browser=chrome --define headless=true
```

Accès dans le code :

```python
browser = context.config.userdata.get('browser', 'chrome')
```

### Lister tous les scénarios sans les exécuter

```bash
behave --dry-run --no-summary --format=plain
```

---

## Exemples de workflows courants

### Tests de smoke (rapides)

```bash
behave --tags=@smoke -v
```

### Tests de régression complets

```bash
behave --tags=@regression --format=json -o report.json
```

### Développement (avec arrêt au premier échec)

```bash
behave --tags=@wip -x -v
```

### Tests headless (sans interface graphique)

```bash
behave -D headless=true
```

### Génération de rapport HTML complet

```bash
behave --format=html -o reports/report.html --format=json -o reports/report.json
```

### Debug d'un scénario spécifique

```bash
behave features/login.feature:4 -v --no-capture --logging-level=DEBUG
```

---

## Combinaisons utiles

### Test complet avec rapport

```bash
behave -v --format=pretty --format=json -o report.json --junit --junit-directory=reports/
```

### Mode développement

```bash
behave --tags=@wip -x -v --no-capture
```

### CI/CD (Intégration Continue)

```bash
behave --tags=~@manual --format=json -o report.json --junit --no-capture
```

---

## Fichier behave.ini (configuration)

Créez un fichier `behave.ini` à la racine pour éviter de répéter les options :

```ini
[behave]
format = pretty
show_timings = true
show_skipped = false
logging_level = INFO
junit = true
junit_directory = reports/
```

Ensuite, lancez simplement :

```bash
behave
```

---

## Aide et documentation

### Afficher l'aide complète

```bash
behave --help
behave -h
```

### Version de Behave

```bash
behave --version
```

---

## Tips supplémentaires

- Utilisez `@wip` (Work In Progress) pour les tests en développement
- Utilisez `@skip` pour ignorer temporairement des tests
- Utilisez `@slow` pour marquer les tests lents
- Combinez les tags pour une meilleure organisation

**Exemple de feature avec tags :**

```gherkin
@web @smoke
Feature: Login functionality

  @positive
  Scenario: Successful login
    Given I am on the login page
    ...

  @negative @wip
  Scenario: Login with invalid credentials
    Given I am on the login page
    ...
```

## Allure

### Générer un rapport Allure

```bash
behave --format=allure_behave.formatter:AllureFormatter -o allure-results/
```

### Visualiser le rapport Allure

```bash
allure serve allure-results/
```

### Générer un rapport Allure dynamique

```bash
allure generate allure-results/ -o allure-report/ --clean
```

Ouvrir le rapport dans un navigateur

```bash
allure open allure-report/
```
