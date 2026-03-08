Feature: Navigation et Détails Produits

  Background: Connexion préalable
    Given l'utilisateur est connecté avec "<username>" et "secret_sauce"
    And l'utilisateur est sur la page "/inventory.html"

  @tc-cat-35 @PSD-116 @web @critical @navigation @epic-PSD-95
  Scenario Outline: TC-CAT-35 - Accès détail produit via le nom - Utilisateur: <username>
    When l'utilisateur clique sur le nom du produit "Sauce Labs Backpack"
    Then l'utilisateur est redirigé vers la fiche produit "/inventory-item.html?id=4"
    And le nom "Sauce Labs Backpack" est affiché
    And le prix "$29.99" est visible
    And l'image agrandie du produit est visible avec le alt "Sauce Labs Backpack"
    And la description du produit est affichée
    Examples:
      | username      |
      | standard_user |
      | problem_user  |

  @tc-cat-34 @PSD-115 @web @high @navigation @epic-PSD-95
  Scenario Outline: TC-CAT-34 - Accès détail produit via l'image - Utilisateur: <username>
    When l'utilisateur clique sur l'image du produit "Sauce Labs Backpack"
    Then l'utilisateur est redirigé vers la fiche produit "/inventory-item.html?id=4"
    And le nom "Sauce Labs Backpack" est affiché
    And le prix "$29.99" est visible
    And l'image agrandie du produit est visible avec le alt "Sauce Labs Backpack"
    And la description du produit est affichée
    Examples:
      | username      |
      | standard_user |
      | problem_user  |

