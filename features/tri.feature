# couvre le point 7 (Tri A-Z, Z-A, Prix).

Feature: Tri du Catalogue Produits

  Background: Connexion préalable
    Given l'utilisateur est connecté avec "<username>" et "secret_sauce"
    And l'utilisateur est sur la page "/inventory.html"

  @tc-cat-36 @PSD-118 @web @medium @sort @epic-PSD-95
  Scenario Outline: TC-CAT-36 - Tri par nom (A à Z) depuis un ordre différent - Utilisateur: <username>
    Given l'utilisateur sélectionne l'option de tri "Name (Z to A)"
    When l'utilisateur sélectionne l'option de tri "Name (A to Z)"
    Then les produits avec leurs noms sont affichés dans cet ordre :
      | nom_produit                        |
      | Sauce Labs Backpack                |
      | Sauce Labs Bike Light              |
      | Sauce Labs Bolt T-Shirt            |
      | Sauce Labs Fleece Jacket           |
      | Sauce Labs Onesie                  |
      | Test.allTheThings() T-Shirt (Red)  |

    Examples:
      | username      |
      | standard_user |
      | problem_user  |

  @tc-cat-37 @PSD-119 @web @medium @sort @epic-PSD-95
  Scenario Outline: TC-CAT-37 - Tri par nom (Z à A) - Utilisateur: <username>
    Given le texte du sélecteur de tri affiche "Name (A to Z)"
    When l'utilisateur sélectionne l'option de tri "Name (Z to A)"
    Then les produits avec leurs noms sont affichés dans cet ordre :
      | nom_produit                        |
      | Test.allTheThings() T-Shirt (Red)  |
      | Sauce Labs Onesie                  |
      | Sauce Labs Fleece Jacket           |
      | Sauce Labs Bolt T-Shirt            |
      | Sauce Labs Bike Light              |
      | Sauce Labs Backpack                |
    
    Examples:
      | username      |
      | standard_user |
      | problem_user  |

  @tc-cat-38 @PSD-120 @web @medium @sort @epic-PSD-95
  Scenario Outline: TC-CAT-38 - Tri par prix (Low to High) - Utilisateur: <username>
    When l'utilisateur sélectionne l'option de tri "Price (low to high)"
    Then les produits avec leurs noms et leurs prix sont affichés dans cet ordre :
      | nom_produit                        | prix  |
      | Sauce Labs Onesie                  | $7.99 |
      | Sauce Labs Bike Light              | $9.99 |
      | Sauce Labs Bolt T-Shirt            | $15.99|
      | Test.allTheThings() T-Shirt (Red)  | $15.99|
      | Sauce Labs Backpack                | $29.99|
      | Sauce Labs Fleece Jacket           | $49.99|

    Examples:
      | username      |
      | standard_user |
      | problem_user  |

  @tc-cat-39 @PSD-121 @web @medium @sort @epic-PSD-95
  Scenario Outline: TC-CAT-39 - Tri par prix (High to Low) - Utilisateur: <username>
    When l'utilisateur sélectionne l'option de tri "Price (high to low)"
    Then les produits avec leurs noms et leurs prix sont affichés dans cet ordre :
      | nom_produit                        | prix  |
      | Sauce Labs Fleece Jacket           | $49.99|
      | Sauce Labs Backpack                | $29.99|
      | Sauce Labs Bolt T-Shirt            | $15.99|
      | Test.allTheThings() T-Shirt (Red)  | $15.99|
      | Sauce Labs Bike Light              | $9.99 |
      | Sauce Labs Onesie                  | $7.99 |

    Examples:
      | username      |
      | standard_user |
      | problem_user  |