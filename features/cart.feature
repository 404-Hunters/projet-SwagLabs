# ============================================================
# Feature: Gestion du Panier & Tunnel de Commande
# Application: SauceDemo (https://www.saucedemo.com)
# Exécuté par: Hamza
# Date: 20/02/2026
# ============================================================

Feature: Gestion du Panier - CART

  Background: Connexion préalable
    Given je suis connecté avec "standard_user" et "secret_sauce"
    And je suis sur la page "/inventory.html"


  # ============================================================
  # STORY-03 : Gestion du Panier
  # ============================================================

  # TC-CART-01
  @TC-CART-01 @web @high @panier
    Scenario: Ajout d'un produit depuis la page d'accueil
    When l'utilisateur clique sur le bouton "Add to cart" du produit "Sauce Labs Backpack"
    Then le bouton du produit "Sauce Labs Backpack" affiche "Remove"
    And le badge rouge du panier affiche "1"

  # TC-CART-02
  @TC-CART-02 @web @high @panier
  Scenario Outline: Ajout d'un produit depuis la fiche détail
    Given je suis sur la page de détail du produit "<nom_produit>"
    When l'utilisateur clique sur le bouton "Add to cart" depuis la fiche détail
    Then le bouton "Add to cart" de la fiche détail affiche "Remove"
    And le badge rouge du panier affiche "1"

    Examples: Produits
      | nom_produit           |
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
      | Sauce Labs Onesie     |

  # TC-CART-03
  @TC-CART-03 @web @medium @panier
  Scenario: Ajout de tous les produits (6 articles)
    Given l'utilisateur est connecté en tant que "standard_user"
    And l'utilisateur est sur la page Inventory "https://www.saucedemo.com/inventory.html"
    And le panier est vide
    When l'utilisateur clique sur "Add to cart" pour chacun des 6 produits disponibles
    Then tous les boutons des produits affichent "Remove"
    And le badge rouge du panier affiche "6"
    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "https://www.saucedemo.com/cart.html"
    And le panier contient exactement 6 produits

  # TC-CART-06
  @TC-CART-06 @web @high @panier
  Scenario: Suppression d'un article depuis la page Panier
    Given l'utilisateur a au moins 1 produit dans le panier
    When l'utilisateur clique sur l'icône "shopping cart" pour accéder à la page Panier
    And l'utilisateur clique sur le bouton "Remove" depuis la page Panier
    Then le produit est retiré de la liste du panier
    And le badge rouge du panier est décrémenté