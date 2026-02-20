# ============================================================
# Feature: Tunnel de Commande - Paiement & Succès
# Application: SauceDemo (https://www.saucedemo.com)
# Exécuté par: Hamza
# Date: 20/02/2026
# ============================================================

Feature: Tunnel de Commande - Paiement et Succès

  Background:
    Given l'utilisateur est connecté en tant que "standard_user"
    And l'utilisateur a au moins 1 produit dans le panier
    And l'utilisateur a rempli les informations de livraison avec "John", "Doe", "12345"
    And l'utilisateur est sur la page "Checkout: Overview" "https://www.saucedemo.com/checkout-step-two.html"


  # ============================================================
  # STORY-05 : Tunnel de Commande - Paiement & Succès
  # ============================================================

  # TC-CHECK-08
  @TC-CHECK-08 @web @high @checkout @parcours-complet
  Scenario: Parcours de commande complet
    Given le panier contient le produit "Sauce Labs Backpack"
    And l'utilisateur est sur la page Inventory "https://www.saucedemo.com/inventory.html"
    When l'utilisateur clique sur "Add to cart" pour le produit "Sauce Labs Backpack"
    And l'utilisateur accède à la page Panier
    And l'utilisateur clique sur "Checkout"
    And l'utilisateur saisit "John" dans "First Name", "Doe" dans "Last Name", "12345" dans "Zip/Postal Code"
    And l'utilisateur clique sur "Continue"
    And l'utilisateur clique sur "Finish"
    Then l'utilisateur est redirigé vers la page de confirmation de commande
    And le message "Thank you for your order!" est affiché