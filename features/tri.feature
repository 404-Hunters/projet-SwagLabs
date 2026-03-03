# couvre le point 7 (Tri A-Z, Z-A, Prix).

Feature: Tri du Catalogue Produits

  Background: Connexion préalable
    Given je suis connecté avec "standard_user" et "secret_sauce"
    And je suis sur la page "/inventory.html"

  @tc-cat-36 @web @medium @sort
  Scenario: TC-CAT-36 - Tri par nom (A à Z) depuis un ordre différent
    Given je sélectionne l'option de tri "Name (Z to A)"
    When je sélectionne l'option de tri "Name (A to Z)"
    Then les produits sont affichés dans cet ordre :
      | Sauce Labs Backpack                |
      | Sauce Labs Bike Light              |
      | Sauce Labs Bolt T-Shirt            |
      | Sauce Labs Fleece Jacket           |
      | Sauce Labs Onesie                  |
      | Test.allTheThings() T-Shirt (Red)  |

  @tc-cat-37 @web @medium @sort
  Scenario: TC-CAT-37 - Tri par nom (Z à A)
    Given le texte du sélecteur de tri affiche "Name (A to Z)"
    When je sélectionne l'option de tri "Name (Z to A)"
    Then les produits sont affichés dans cet ordre :
      | Test.allTheThings() T-Shirt (Red)  |
      | Sauce Labs Onesie                  |
      | Sauce Labs Fleece Jacket           |
      | Sauce Labs Bolt T-Shirt            |
      | Sauce Labs Bike Light              |
      | Sauce Labs Backpack                |

  @tc-cat-38 @web @medium @sort
  Scenario: TC-CAT-38 - Tri par prix (Low to High)
    When je sélectionne l'option de tri "Price (low to high)"
    Then les produits sont affichés dans cet ordre :
      | Nom produit                        | Prix  |
      | Sauce Labs Onesie                  | $7.99 |
      | Sauce Labs Bike Light              | $9.99 |
      | Sauce Labs Bolt T-Shirt            | $15.99|
      | Test.allTheThings() T-Shirt (Red)  | $15.99|
      | Sauce Labs Backpack                | $29.99|
      | Sauce Labs Fleece Jacket           | $49.99|

  @tc-cat-39 @web @medium @sort
  Scenario: TC-CAT-39 - Tri par prix (High to Low)
    When je sélectionne l'option de tri "Price (high to low)"
    Then les produits sont affichés dans cet ordre :
      | Nom produit                        | Prix  |
      | Sauce Labs Fleece Jacket           | $49.99|
      | Sauce Labs Backpack                | $29.99|
      | Sauce Labs Bolt T-Shirt            | $15.99|
      | Test.allTheThings() T-Shirt (Red)  | $15.99|
      | Sauce Labs Bike Light              | $9.99 |
      | Sauce Labs Onesie                  | $7.99 |
