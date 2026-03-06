# couvre les points 1, 2, 10 et 3 (Connexion standard, Locked_out_user, Champs vides login, Logout).

Feature: Authentification sur SauceDemo

  @tc-auth-01 @web @critical @smoke
  Scenario Outline: TC-AUTH-01 - Connexion avec différents types d'utilisateurs
    Given l'utilisateur est sur la page Login
    When l'utilisateur saisit "<nom_utilisateur>" dans le champ "Username"
    And l'utilisateur saisit "secret_sauce" dans le champ "Password"
    And l'utilisateur clique sur le bouton "Login"
    Then l'utilisateur est redirigé vers la page "/inventory.html"
    And la liste des produits est affichée

    Examples:
      | nom_utilisateur   |
      | standard_user     |
      | problem_user      |

  @tc-auth-05 @web @critical @negative
  Scenario: TC-AUTH-05 - Connexion refusée pour locked_out_user
    Given l'utilisateur est sur la page Login
    When l'utilisateur saisit "locked_out_user" dans le champ "Username"
    And l'utilisateur saisit "secret_sauce" dans le champ "Password"
    And l'utilisateur clique sur le bouton "Login"
    Then le message d'erreur "Epic sadface: Sorry, this user has been locked out." est affiché
    And l'utilisateur reste sur la page Login

  @tc-auth-07 @web @high @negative
  Scenario: TC-AUTH-07 - Connexion avec champs vides
    Given l'utilisateur est sur la page Login
    When l'utilisateur laisse le champ "Username" vide
    And l'utilisateur laisse le champ "Password" vide
    And l'utilisateur clique sur le bouton "Login"
    Then le message d'erreur "Epic sadface: Username is required" est affiché
    And l'utilisateur reste sur la page Login

  @tc-auth-10 @web @high @logout
  Scenario Outline: TC-AUTH-10 - Déconnexion réussie (Logout)
    Given l'utilisateur est connecté en tant que "<nom_utilisateur>"
    When l'utilisateur clique sur le menu "Burger"
    And l'utilisateur clique sur le lien "Logout"
    Then l'utilisateur est redirigé vers la page Login

    Examples:
      | nom_utilisateur   |
      | standard_user     |
      | problem_user      |
