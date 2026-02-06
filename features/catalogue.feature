Feature: Parcours du catalogue produit
    En tant que client
    Je veux pouvoir consulter et rechercher des produits dans le catalogue,
    Afin de trouver facilement les articles que je souhaite acheter.

    Scenario: Consultation du catalogue produit
        Given un utilisateur connecté
        When l'utilisateur accède à la page du catalogue produits
        Then il devrait voir une liste de produits disponibles avec leurs noms, descriptions et prix

    Scenario: Recherche de produit par nom
        Given un utilisateur connecté
        When l'utilisateur recherche un produit avec le nom "Chaussures de sport"
        Then il devrait voir une liste de produits correspondant à la recherche avec leurs noms, descriptions et prix
