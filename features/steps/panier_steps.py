from behave import given, when, then

# ===== Scenario: Ajouter un produit au panier =====

@when("l'utilisateur ajoute le produit avec l'ID \"{product_id}\" au panier et son intitulé \"{nom_produit}\"")
def step_when_utilisateur_ajoute_produit_panier(context, product_id, nom_produit):
    if not hasattr(context, 'panier'):
        context.panier = []
    produit = {"id": product_id, "nom": nom_produit, "quantite": 1}
    context.panier.append(produit)

@then("le panier devrait contenir le produit avec l'ID \"{product_id}\" et son intitulé \"{nom_produit}\"")
def step_then_panier_contient_produit(context, product_id, nom_produit):
    produit_trouve = any(
        produit for produit in context.panier
        if produit["id"] == product_id and produit["nom"] == nom_produit
    )
    assert produit_trouve, f"Le produit avec l'ID {product_id} et l'intitulé {nom_produit} n'est pas dans le panier."


# ===== Scenario: Supprimer un produit du panier =====
@given("le produit avec l'ID \"{product_id}\" dans son panier")
def step_given_produit_dans_panier(context, product_id):
    if not hasattr(context, 'panier'):
        context.panier = []
    produit = {"id": product_id, "nom": "Produit Exemple", "quantite": 1}
    context.panier.append(produit)

@when("l'utilisateur supprime le produit avec l'ID \"{product_id}\" du panier")
def step_when_utilisateur_supprime_produit_panier(context, product_id):
    context.panier = [
        produit for produit in context.panier
        if produit["id"] != product_id
    ]

@then("le panier ne devrait plus contenir le produit avec l'ID \"{product_id}\"")
def step_then_panier_ne_contient_plus_produit(context, product_id):
    produit_trouve = any(
        produit for produit in context.panier
        if produit["id"] == product_id
    )
    assert not produit_trouve, f"Le produit avec l'ID {product_id} est toujours dans le panier."


# ===== Scenario: Calculer le total du panier =====
@given("le panier contient les produits suivants: ")
def step_given_panier_contient_produits(context):
    context.panier = []
    for row in context.table:
        produit = {
            "id": row['product_id'],
            "nom": row['product_name'],
            "prix": float(row['price'])
        }
        context.panier.append(produit)