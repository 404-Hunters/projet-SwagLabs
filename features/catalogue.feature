#couvre ton point 8 (Consultation détail produit) et la vérification des éléments.

Feature: Navigation et Détails Produits

  Background: Connexion préalable
    Given je suis connecté avec "standard_user" et "secret_sauce"

  @tc-cat-35 @web @critical @navigation
  Scenario: TC-CAT-35 - Accès détail produit via le nom
    Given je suis connecté sur la page "/inventory.html"
    When je clique sur le nom du produit "Sauce Labs Backpack"
    Then je suis redirigé vers la fiche produit "/inventory-item.html?id=4"
    And le nom "Sauce Labs Backpack" est affiché
    And le prix "$29.99" est visible
    And la description du produit est affichée

  @tc-cat-34 @web @high @navigation
  Scenario: TC-CAT-34 - Accès détail produit via l'image
    Given je suis connecté sur la page "/inventory.html"
    When je clique sur l'image du produit "Sauce Labs Backpack"
    Then je suis redirigé vers la fiche produit "/inventory-item.html?id=4"
    And l'image agrandie du produit est visible
    And le prix "$29.99" est visible
    And la description du produit est affichée
