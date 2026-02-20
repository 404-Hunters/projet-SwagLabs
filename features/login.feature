# couvre les points 1, 2, 10 et 3 (Connexion standard, Locked_out_user, Champs vides login, Logout).

Feature: Authentification sur SauceDemo

  @tc-auth-01 @web @critical @smoke
  Scenario: TC-AUTH-01 - Connexion réussie avec standard_user
    Given je suis sur la page Login
    When je saisis "standard_user" dans le champ "Username"
    And je saisis "secret_sauce" dans le champ "Password"
    And je clique sur le bouton "Login"
    Then je suis redirigé vers la page "/inventory.html"
    And la liste des produits est affichée

  @tc-auth-05 @web @critical @negative
  Scenario: TC-AUTH-05 - Connexion refusée pour locked_out_user
    Given je suis sur la page Login
    When je saisis "locked_out_user" dans le champ "Username"
    And je saisis "secret_sauce" dans le champ "Password"
    And je clique sur le bouton "Login"
    Then le message d'erreur "Epic sadface: Sorry, this user has been locked out." est affiché
    And je reste sur la page Login

  @tc-auth-07 @web @high @negative
  Scenario: TC-AUTH-07 - Connexion avec champs vides
    Given je suis sur la page Login
    When je laisse le champ "Username" vide
    And je laisse le champ "Password" vide
    And je clique sur le bouton "Login"
    Then le message d'erreur "Epic sadface: Username is required" est affiché
    And je reste sur la page Login

  @tc-auth-10 @web @high @logout
  Scenario: TC-AUTH-10 - Déconnexion réussie (Logout)
    Given je suis connecté en tant que "standard_user"
    When je clique sur le menu "Burger"
    And je clique sur le lien "Logout"
    Then je suis redirigé vers la page Login
