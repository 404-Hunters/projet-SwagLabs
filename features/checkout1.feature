# ============================================================
# Feature: Tunnel de Commande - Coordonnées
# Application: SauceDemo (https://www.saucedemo.com)
# Exécuté par: Hamza
# Date: 20/02/2026
# ============================================================

Feature: Tunnel de Commande - Coordonnées

  Background:
    Given l'utilisateur est connecté en tant que "standard_user"
    And l'utilisateur a au moins 1 produit dans le panier
    And l'utilisateur est sur la page Panier "https://www.saucedemo.com/cart.html"


  # ============================================================
  # STORY-04 : Tunnel de Commande - Coordonnées
  # ============================================================

  # TC-CHECK-06
  @TC-CHECK-06 @web @medium @checkout @validation
  Scenario: Soumission avec tous les champs vides
    Given l'utilisateur est sur la page "https://www.saucedemo.com/checkout-step-one.html"
    When l'utilisateur laisse tous les champs vides
    And l'utilisateur clique sur le bouton "Continue"
    Then un message d'erreur "Error: First Name is required" est affiché
    And un message d'erreur "Error: Last Name is required" est affiché
    And un message d'erreur "Error: Postal Code is required" est affiché
    And l'utilisateur reste sur la page "Checkout: Your Information"