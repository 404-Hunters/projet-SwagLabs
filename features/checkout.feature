# ============================================================
# Feature: Commande & Tunnel de Commande
# Application: SauceDemo (https://www.saucedemo.com)
# Exécuté par: Hamza
# Date: 20/02/2026
# ============================================================

Feature: Commande & Tunnel de Commande

  Background:
    Given l'utilisateur est connecté en tant que "standard_user"
    And l'article "Sauce Labs Backpack" est présent dans le panier

  # TC-CHECK-06
  @TC-CHECK-06 @web @medium @checkout @validation
  Scenario: Soumission avec tous les champs vides
    Given l'utilisateur est sur la page "/checkout-step-one.html"
    When l'utilisateur clique sur le bouton "Continue" de la page Checkout "checkout-step-one"
    Then un seul message d'erreur "Error: First Name is required" est affiché
    And l'utilisateur reste sur la page "/checkout-step-one.html"

  # TC-CHECK-08
  @TC-CHECK-08 @web @high @checkout @parcours-complet @smoke
  Scenario: Parcours de commande complet
    Given l'utilisateur est sur la page "/checkout-step-one.html"
      When l'utilisateur remplit le formulaire de commande:
      | champ           | valeur |
      | First Name      | John   |
      | Last Name       | Doe    |
      | Zip/Postal Code | 12345  |
    And l'utilisateur clique sur le bouton "Continue" de la page Checkout "checkout-step-one"
    Then l'utilisateur est redirigé vers la page "/checkout-step-two.html"
    When l'utilisateur clique sur le bouton "Finish" de la page Checkout "checkout-step-two"
    Then l'utilisateur est redirigé vers la page "/checkout-complete.html"
    Then le message de confirmation "Thank you for your order!" est affiché