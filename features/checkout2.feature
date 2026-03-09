# ============================================================
# Feature: Commande & Calcul du Total
# Application: SauceDemo (https://www.saucedemo.com)
# Exécuté par: Quentin
# Date: 20/02/2026
# ============================================================

Feature: Commande & Calcul du Total

  Background:
    Given l'utilisateur est connecté avec "<username>" et "secret_sauce"
    And l'utilisateur est sur la page "/inventory.html"
    And le panier contient les produits suivants:
      | produit                  | quantité | prix unitaire |
      | Sauce Labs Backpack      | 1        | 29.99         |
      | Sauce Labs Bike Light    | 1        | 9.99          |
      | Sauce Labs Bolt T-Shirt  | 1        | 15.99         |
      | Sauce Labs Fleece Jacket | 1        | 49.99         |

  # TC-CHECK-10
  @TC-CHECK-10 @web @medium @checkout @calcul_total
  Scenario Outline: TC-CHECK-10 Vérification du calcul du total de la commande sans taxe - Utilisateur: <username>
    Given l'utilisateur est sur la page "/checkout-step-one.html"
    When l'utilisateur remplit le formulaire de commande:
      | champ           | valeur |
      | First Name      | John   |
      | Last Name       | Doe    |
      | Zip/Postal Code | 12345  |
    And l'utilisateur clique sur le bouton "Continue" de la page Checkout "checkout-step-one"
    Then l'utilisateur est redirigé vers la page "/checkout-step-two.html"
    And le total des prix de la commande sans taxe affiche "105.96"

    Examples:
      | username      |
      | standard_user |

  # TC-CHECK-11 : Calcul de la taxe (8%)
  @TC-CHECK-11 @web @medium @checkout @calcul_total
  Scenario Outline: TC-CHECK-11 Vérification du calcul de la taxe (8%) - Utilisateur: <username>
    Given l'utilisateur est sur la page "/checkout-step-one.html"
    When l'utilisateur remplit le formulaire de commande:
      | champ           | valeur |
      | First Name      | John   |
      | Last Name       | Doe    |
      | Zip/Postal Code | 12345  |
    And l'utilisateur clique sur le bouton "Continue" de la page Checkout "checkout-step-one"
    Then l'utilisateur est redirigé vers la page "/checkout-step-two.html"
    And le montant de la taxe affiche "8.48"

    Examples:
      | username      |
      | standard_user |

  # TC-CHECK-12 : Vérification du total de la commande avec taxe
  @TC-CHECK-12 @PSD-161 @web @medium @checkout @calcul_total @epic-PSD-94
  Scenario Outline: TC-CHECK-12 Vérification du total de la commande avec taxe - Utilisateur: <username>
    Given l'utilisateur est sur la page "/checkout-step-one.html"
    When l'utilisateur remplit le formulaire de commande:
      | champ           | valeur |
      | First Name      | John   |
      | Last Name       | Doe    |
      | Zip/Postal Code | 12345  |
    And l'utilisateur clique sur le bouton "Continue" de la page Checkout "checkout-step-one"
    Then l'utilisateur est redirigé vers la page "/checkout-step-two.html"
    And le total de la commande avec taxe affiche "114.44"

    Examples:
      | username      |
      | standard_user |
      | problem_user  |