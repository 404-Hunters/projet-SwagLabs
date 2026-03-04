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
  @TC-CART-01 @high @panier @web
  Scenario Outline: Ajout d'un produit depuis la page d'accueil
    Given le panier est vide
    When l'utilisateur clique sur le bouton "Add to cart" de l'article "<nom_produit>"
    Then le bouton de l'article "<nom_produit>" affiche "Remove"
    And le badge rouge du panier affiche "1"
    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "/cart.html"
    And le panier contient l'article "<nom_produit>"

    Examples: Produits
    | nom_produit           |
    | Sauce Labs Backpack   |
    | Sauce Labs Bike Light |
    | Sauce Labs Onesie     |


  # TC-CART-02
  @TC-CART-02 @web @high @panier
  Scenario Outline: Ajout d'un produit depuis la fiche détail
    Given je suis sur la page de détail du produit "<nom_produit>"
    When l'utilisateur clique sur le bouton "Add to cart" depuis la fiche détail
    Then le bouton de l'article "<nom_produit>" sur la page détail affiche "Remove"
    And le badge rouge du panier affiche "1"

    Examples: Produits
      | nom_produit           |
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
      | Sauce Labs Onesie     |

  # TC-CART-03
  @TC-CART-03 @web @medium @panier
  Scenario: Ajout de tous les produits (6 articles)
    Given le panier est vide

    When l'utilisateur clique sur "Add to cart" pour chacun des 6 produits disponibles
    Then tous les boutons des produits affichent "Remove"
    And le badge rouge du panier affiche "6"

    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "/cart.html"
    And le panier contient exactement 6 produits


  # TC-CART-05
  @TC-CART-05 @P1 @web @critique @panier
  Scenario Outline: Suppression d'un article depuis la page d'accueil
    Given l'article "<nom_produit>" est présent dans le panier
    And le bouton de l'article "<nom_produit>" affiche "Remove"

    When l'utilisateur clique sur le bouton "Remove" de l'article "<nom_produit>"
    Then le bouton de l'article "<nom_produit>" affiche "Add to cart"
    And le badge du panier disparaît

    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "/cart.html"
    And le panier est vide

    Examples: Produits
      | nom_produit           |
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
      | Sauce Labs Onesie     |

     
  # TC-CART-06
  @TC-CART-06 @web @high @panier
  Scenario Outline: Suppression d'un article depuis la page Panier
    Given l'article "<nom_produit>" est présent dans le panier
    And le bouton de l'article "<nom_produit>" affiche "Remove"

    When l'utilisateur clique sur l'icône du panier
    Then l'utilisateur est redirigé vers la page Panier "/cart.html"
    And le bouton de l'article "<nom_produit>" affiche "Remove"

    When l'utilisateur clique sur le bouton "Remove" de l'article "<nom_produit>" 
    Then l'article "<nom_produit>" est retiré de la liste du panier
    And le badge du panier disparaît
    And le panier est vide

    Examples: Produits
      | nom_produit           |
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |
      | Sauce Labs Onesie     |
