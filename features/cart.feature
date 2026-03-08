# ============================================================
# Feature: Gestion du Panier & Tunnel de Commande
# Application: SauceDemo (https://www.saucedemo.com)
# Exécuté par: Hamza
# Date: 20/02/2026
# ============================================================

Feature: Gestion du Panier - CART

  Background: Connexion préalable
    Given l'utilisateur est connecté avec "<username>" et "secret_sauce"
    And l'utilisateur est sur la page "/inventory.html"


  # ============================================================
  # STORY-03 : Gestion du Panier
  # ============================================================


  # TC-CART-01
  @TC-CART-01 @PSD-143 @high @panier @web @epic-PSD-94
  Scenario Outline: Ajout d'un produit depuis la page d'accueil - Utilisateur: <username>
    Given le panier est vide
    When l'utilisateur clique sur le bouton "Add to cart" de l'article "<nom_produit>"
    Then le bouton de l'article "<nom_produit>" affiche "Remove"
    And le badge rouge du panier affiche "1"
    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "/cart.html"
    And le panier contient l'article "<nom_produit>"

    Examples:
    | nom_produit           | username      |
    | Sauce Labs Backpack   | standard_user |
    | Sauce Labs Bike Light | standard_user |
    | Sauce Labs Onesie     | standard_user |
    | Sauce Labs Backpack   | problem_user  |
    | Sauce Labs Bike Light | problem_user  |
    | Sauce Labs Onesie     | problem_user  |


  # TC-CART-02
  @TC-CART-02 @PSD-144 @web @high @panier @epic-PSD-94
  Scenario Outline: Ajout d'un produit depuis la fiche détail - Utilisateur: <username>
    Given l'utilisateur est sur la page de détail du produit "<nom_produit>"
    When l'utilisateur clique sur le bouton "Add to cart" depuis la fiche détail
    Then le bouton de l'article "<nom_produit>" sur la page détail affiche "Remove"
    And le badge rouge du panier affiche "1"

    Examples:
      | nom_produit           | username      |
      | Sauce Labs Backpack   | standard_user |
      | Sauce Labs Bike Light | standard_user |
      | Sauce Labs Onesie     | standard_user |
      | Sauce Labs Backpack   | problem_user  |
      | Sauce Labs Bike Light | problem_user  |
      | Sauce Labs Onesie     | problem_user  |

  # TC-CART-03
  @TC-CART-03 @PSD-145 @web @medium @panier @epic-PSD-94
  Scenario Outline: Ajout de tous les produits (6 articles) - Utilisateur: <username>
    Given le panier est vide

    When l'utilisateur clique sur "Add to cart" pour chacun des 6 produits disponibles
    Then tous les boutons des produits affichent "Remove"
    And le badge rouge du panier affiche "6"

    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "/cart.html"
    And le panier contient exactement 6 produits

    Examples:
      | username      |
      | standard_user |
      | problem_user  |


  # TC-CART-05
  @TC-CART-05 @PSD-147 @web @critique @panier @epic-PSD-94
  Scenario Outline: Suppression d'un article depuis la page d'accueil - Utilisateur: <username>
    Given l'article "<nom_produit>" est présent dans le panier
    And le bouton de l'article "<nom_produit>" affiche "Remove"

    When l'utilisateur clique sur le bouton "Remove" de l'article "<nom_produit>"
    Then le bouton de l'article "<nom_produit>" affiche "Add to cart"
    And le badge du panier disparaît

    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "/cart.html"
    And le panier est vide

    Examples:
      | nom_produit           | username      |
      | Sauce Labs Backpack   | standard_user |
      | Sauce Labs Bike Light | standard_user |
      | Sauce Labs Onesie     | standard_user |
      | Sauce Labs Backpack   | problem_user  |
      | Sauce Labs Bike Light | problem_user  |
      | Sauce Labs Onesie     | problem_user  |

     
  # TC-CART-06
  @TC-CART-06 @PSD-148 @web @high @panier @epic-PSD-94
  Scenario Outline: Suppression d'un article depuis la page Panier - Utilisateur: <username>
    Given l'article "<nom_produit>" est présent dans le panier
    And le bouton de l'article "<nom_produit>" affiche "Remove"

    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "/cart.html"
    And le bouton de l'article "<nom_produit>" affiche "Remove"

    When l'utilisateur clique sur le bouton "Remove" de l'article "<nom_produit>" 
    Then l'article "<nom_produit>" est retiré de la liste du panier
    And le badge du panier disparaît
    And le panier est vide

    Examples:
      | nom_produit           | username      |
      | Sauce Labs Backpack   | standard_user |
      | Sauce Labs Bike Light | standard_user |
      | Sauce Labs Onesie     | standard_user |
      | Sauce Labs Backpack   | problem_user  |
      | Sauce Labs Bike Light | problem_user  |
      | Sauce Labs Onesie     | problem_user  |
