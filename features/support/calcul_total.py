# support/calcul_total.py

TAX_RATE = 0.08  # 8% sur SauceDemo

produits = [
    {"produit": "Sauce Labs Backpack",      "quantité": 1, "prix": 29.99},
    {"produit": "Sauce Labs Bike Light",    "quantité": 1, "prix":  9.99},
    {"produit": "Sauce Labs Bolt T-Shirt",  "quantité": 1, "prix": 15.99},
    {"produit": "Sauce Labs Fleece Jacket", "quantité": 1, "prix": 49.99},
]

sous_total = round(sum(p["quantité"] * p["prix"] for p in produits), 2)
taxe       = round(sous_total * TAX_RATE, 2)
total      = round(sous_total + taxe, 2)

print(f'And le sous-total affiché est "${sous_total}"')
print(f'And la taxe affichée est "${taxe}"')
print(f'And le total affiché est "${total}"')