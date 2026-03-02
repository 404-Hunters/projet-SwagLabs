# couvre le point 7 (Tri A-Z, Z-A, Prix).

Feature: Tri du Catalogue Produits

  Background: Connexion préalable
    Given je suis connecté avec "standard_user" et "secret_sauce"
    And je suis sur la page "/inventory.html"
  
  @tc-cat-36 @web @medium @sort
  Scenario: TC-CAT-36 - Tri par nom (A à Z) depuis un ordre différent
    Given je sélectionne l'option de tri "Name (Z to A)"
    When je sélectionne l'option de tri "Name (A to Z)"
    Then le premier produit affiché est "Sauce Labs Backpack"
    And le troisième produit affiché est "Sauce Labs Bolt T-Shirt"
    And le dernier produit affiché est "Test.allTheThings() T-Shirt (Red)"

  @tc-cat-37 @web @medium @sort
  Scenario: TC-CAT-37 - Tri par nom (Z à A)
    Given le texte du sélecteur de tri affiche "Name (A to Z)"
    When je sélectionne l'option de tri "Name (Z to A)"
    Then le premier produit affiché est "Test.allTheThings() T-Shirt (Red)"
    And le troisième produit affiché est "Sauce Labs Fleece Jacket"
    And le dernier produit affiché est "Sauce Labs Backpack"

  @tc-cat-38 @web @medium @sort
  Scenario: TC-CAT-38 - Tri par prix (Low to High)
    When je sélectionne l'option de tri "Price (low to high)"
    Then le premier produit affiché est "Sauce Labs Onesie"
    And le troisième produit affiché est "Sauce Labs Bolt T-Shirt"
    And le dernier produit affiché est "Sauce Labs Fleece Jacket"


  @tc-cat-39 @web @medium @sort
  Scenario: TC-CAT-39 - Tri par prix (High to Low)
    When je sélectionne l'option de tri "Price (high to low)"
    Then le premier produit affiché est "Sauce Labs Fleece Jacket"
    And le troisième produit affiché est "Sauce Labs Bolt T-Shirt"
    And le dernier produit affiché est "Sauce Labs Onesie"

