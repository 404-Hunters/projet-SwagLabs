@web @tc-auth-01 @critical @smoke
Feature: Authentification

  Scenario: Connexion réussie avec standard_user

    Given je suis sur la page Login
    
    When je saisis "standard_user" dans le champ "Username"
    And je saisis "secret_sauce" dans le champ "Password"
    And je clique sur le bouton "Login"
    
    Then je suis redirigé vers la page "/inventory.html"
    And la liste des produits est affichée