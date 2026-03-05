Feature: Navigation et Détails Produits

  Background: Connexion préalable
    Given l'utilisateur est connecté avec "standard_user" et "secret_sauce"

  @tc-cat-35 @web @critical @navigation
  Scenario: TC-CAT-35 - Accès détail produit via le nom
    Given l'utilisateur est sur la page "/inventory.html"
    When l'utilisateur clique sur le nom du produit "Sauce Labs Backpack"
    Then l'utilisateur est redirigé vers la fiche produit "/inventory-item.html?id=4"
    And le nom "Sauce Labs Backpack" est affiché
    And le prix "$29.99" est visible
    And l'image agrandie du produit est visible avec le alt "Sauce Labs Backpack"
    And la description du produit est affichée

  @tc-cat-34 @web @high @navigation
  Scenario: TC-CAT-34 - Accès détail produit via l'image
    Given l'utilisateur est sur la page "/inventory.html"
    When l'utilisateur clique sur l'image du produit "Sauce Labs Backpack"
    Then l'utilisateur est redirigé vers la fiche produit "/inventory-item.html?id=4"
    And le nom "Sauce Labs Backpack" est affiché
    And le prix "$29.99" est visible
    And l'image agrandie du produit est visible avec le alt "Sauce Labs Backpack"
    And la description du produit est affichée
