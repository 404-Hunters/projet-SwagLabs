# ============================================================
# Feature: Commande & Tunnel de Commande
# Application: SauceDemo (https://www.saucedemo.com)
# Exécuté par: Hamza
# Date: 20/02/2026
# ============================================================

Feature: Commande & Tunnel de Commande

  Background:
    Given l'utilisateur est connecté avec "<username>" et "secret_sauce"
    And l'utilisateur est sur la page "/inventory.html"
    And l'article "Sauce Labs Backpack" est présent dans le panier

  # TC-CHECK-06
  @TC-CHECK-06 @PSD-155 @web @medium @checkout @validation @epic-PSD-94
  Scenario Outline: TC-CHECK-06 - Soumission avec tous les champs vides - Utilisateur: <username>
    Given l'utilisateur est sur la page "/checkout-step-one.html"
    When l'utilisateur clique sur le bouton "Continue" de la page Checkout "checkout-step-one"
    Then un seul message d'erreur "Error: First Name is required" est affiché
    And l'utilisateur reste sur la page "/checkout-step-one.html"

    Examples:
      | username      |
      | standard_user |
      | problem_user  |

  # TC-CHECK-08
  @TC-CHECK-08 @PSD-157 @web @high @checkout @parcours-complet @smoke @epic-PSD-94
  Scenario Outline: TC-CHECK-08 - Parcours de commande complet - Utilisateur: <username>
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
    
    Examples:
      | username      |
      | standard_user |
      | problem_user  |

  


  