Feature: inscription utilisateur
    En tant qu'utilisateur non inscrit,
    Je veux pouvoir m'inscrire sur le site,
    Afin d'accéder aux fonctionnalités réservées aux membres.

    Scenario: Inscription réussie d'un nouvel utilisateur
        Given Je suis sur la page d'inscription
        When Je remplis le formulaire avec mon email : "JohnDoe@email.com"
        And Je remplis le formulaire avec mon mot de passe : "SecurePass123"
        And Je soumets le formulaire d'inscription
        Then Je devrais voir un message de confirmation d'inscription réussie
    
    Scenario: Inscription échouée avec un email déjà utilisé
        Given Je suis sur la page d'inscription
        And l'utilisateur avec l'email "JohnDoe@email.com" existe déjà
        When Je remplis le formulaire avec l'email : "JohnDoe@email.com"
        And Je remplis le formulaire avec mon mot de passe : "AnotherPass456"
        Then Je devrais voir un message d'erreur indiquant que l'email est déjà utilisé

    
