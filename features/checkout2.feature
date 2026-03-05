# ============================================================
# Feature: Commande & Calcul du Total
# Application: SauceDemo (https://www.saucedemo.com)
# Exécuté par: Quentin
# Date: 20/02/2026
# ============================================================

Feature: Commande & Calcul du Total

  Background:
    Given l'utilisateur est connecté en tant que "standard_user"
    And l'utilisateur est sur la page "/inventory.html"
    And le panier contient les produits suivants:
      | produit                  | quantité | prix unitaire |
      | Sauce Labs Backpack      | 1        | 29.99         |
      | Sauce Labs Bike Light    | 1        | 9.99          |
      | Sauce Labs Bolt T-Shirt  | 1        | 15.99         |
      | Sauce Labs Fleece Jacket | 1        | 49.99         |

 # TC-CHECK-10
  @TC-CHECK-10 @web @medium @checkout @calcul_total
  Scenario: Vérification du calcul du total de la commande sans taxe
    Given l'utilisateur est sur la page "/checkout-step-one.html"
    When l'utilisateur remplit le formulaire de commande:
      | champ           | valeur |
      | First Name      | John   |
      | Last Name       | Doe    |
      | Zip/Postal Code | 12345  |
    And l'utilisateur clique sur le bouton "Continue" de la page Checkout "checkout-step-one"
    Then l'utilisateur est redirigé vers la page "/checkout-step-two.html"
    And le total des prix de la commande sans taxe affiche "105.96"
  


  