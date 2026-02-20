# couvre le point 7 (Tri A-Z, Z-A, Prix).

Feature: Tri du Catalogue Produits
  
  @tc-cat-36 @web @medium @sort
  Scenario: TC-CAT-36 - Tri par nom (A à Z) depuis un ordre différent
    Given je suis connecté sur la page "/inventory.html"
    And les produits sont triés par "Name (Z to A)"
    When je sélectionne l'option de tri "Name (A to Z)"
    Then le premier produit affiché est "Sauce Labs Backpack"
    And le dernier produit affiché est "Test.allTheThings() T-Shirt (Red)"


  @tc-cat-37 @web @medium @sort
  Scenario: TC-CAT-37 - Tri par nom (Z à A)
    Given je suis connecté sur la page "/inventory.html"
    When je sélectionne l'option de tri "Name (Z to A)"
    Then le premier produit affiché est "Test.allTheThings() T-Shirt (Red)"
    And le dernier produit affiché est "Sauce Labs Backpack"

  @tc-cat-38 @web @medium @sort
  Scenario: TC-CAT-38 - Tri par prix (Croissant)
    Given je suis connecté sur la page "/inventory.html"
    When je sélectionne l'option de tri "Price (low to high)"
    Then le premier produit affiché est "Sauce Labs Onesie"
    And le dernier produit affiché est "Sauce Labs Fleece Jacket"

  @tc-cat-39 @web @medium @sort
  Scenario: TC-CAT-39 - Tri par prix (Décroissant)
    Given je suis connecté sur la page "/inventory.html"
    When je sélectionne l'option de tri "Price (high to low)"
    Then le premier produit affiché est "Sauce Labs Fleece Jacket"
    And le dernier produit affiché est "Sauce Labs Onesie"
