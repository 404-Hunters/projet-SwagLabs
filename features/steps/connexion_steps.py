from behave import given, when, then

# ===== Scenario: Connexion utilisateur =====
@given("un utilisateur connecté")
def step_given_utilisateur_connecte(context):
    context.utilisateur_connecte = True