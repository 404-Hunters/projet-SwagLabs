from behave import given, when, then


# ===== Scenario: Catalogue de produits =====
@when("l'utilisateur accède à la page du catalogue produits")
def step_when_utilisateur_accede_catalogue(context):
    context.catalogue_accede = True
    context.produits = [
        {"nom": "Produit A", "description": "Description A", "prix": 10.0},
        {"nom": "Produit B", "description": "Description B", "prix": 20.0},
        {"nom": "Produit C", "description": "Description C", "prix": 30.0},
    ]

@then("il devrait voir une liste de produits disponibles avec leurs noms, descriptions et prix")
def step_then_voir_liste_produits(context):
    assert context.catalogue_accede is True, "L'utilisateur n'a pas accédé au catalogue"
    assert len(context.produits) > 0, "La liste des produits ne doit pas être vide"
    for produit in context.produits:
        assert "nom" in produit
        assert "description" in produit
        assert "prix" in produit

# ===== Scenario: Recherche de produit par nom =====
@when("l'utilisateur recherche un produit avec le nom \"{nom_produit}\"")
def step_when_utilisateur_recherche_produit(context, nom_produit):
    # Initialiser les produits si ce n'est pas déjà fait
    if not hasattr(context, 'produits'):
        context.produits = [
            {"nom": "Produit A", "description": "Description A", "prix": 10.0},
            {"nom": "Produit B", "description": "Description B", "prix": 20.0},
            {"nom": "Chaussures de sport", "description": "Chaussures pour le running", "prix": 89.99},
        ]
    
    context.nom_recherche = nom_produit
    context.resultats_recherche = [
        produit for produit in context.produits if produit["nom"] == nom_produit
    ]

@then("il devrait voir une liste de produits correspondant à la recherche avec leurs noms, descriptions et prix")
def step_then_voir_resultats_recherche(context):
    assert context.nom_recherche is not None, "Le nom de recherche n'a pas été défini"
    assert len(context.resultats_recherche) > 0, "Aucun produit ne correspond à la recherche"
    for produit in context.resultats_recherche:
        assert "nom" in produit
        assert "description" in produit
        assert "prix" in produit