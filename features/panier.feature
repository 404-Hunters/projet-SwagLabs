Feature: Gestion d'un panier
    En tant que client,
    Je veux pouvoir ajouter, supprimer et visualiser des produits dans mon panier,
    Afin de gérer mes achats avant de passer à la caisse.

    Scenario Outline: Ajouter un produit au panier
        Given un utilisateur connecté
        When l'utilisateur ajoute le produit avec l'ID "<product_id>" au panier et son intitulé "<product_name>"
        Then le panier devrait contenir le produit avec l'ID "<product_id>" et son intitulé "<product_name>"
        Examples:
            | product_id | product_name       |
            | 101        | Montre connectée   |
            | 202        | Casque audio       |
            | 303        | Smartphone         |


    Scenario Outline: Supprimer un produit du panier
        Given un utilisateur connecté 
        And le produit avec l'ID "<product_id>" dans son panier
        When l'utilisateur supprime le produit avec l'ID "<product_id>" du panier
        Then le panier ne devrait plus contenir le produit avec l'ID "<product_id>"

        Examples:
            | product_id |
            | 101        |
            | 202        |
            | 303        |


    Scenario: Calculer le total du panier
        Given un utilisateur connecté
        And le panier contient les produits suivants:
            | product_id | product_name       | price |
            | 101        | Montre connectée   | 199.99|
            | 202        | Casque audio       | 89.99 |
            | 303        | Smartphone         | 599.99|
        When l'utilisateur consulte le total du panier
        Then le total du panier devrait être de 889.97 euros

