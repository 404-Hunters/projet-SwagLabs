from behave import given, when, then

# ===== Scenario: Inscription utilisateur =====

@given("Je suis sur la page d'inscription")
def step_given_sur_page_inscription(context):
    context.page = "inscription"

@when("Je remplis le formulaire avec mon email : \"{email}\"")
def step_when_remplis_formulaire_email(context, email):
    context.email = email

@when("Je remplis le formulaire avec mon mot de passe : \"{mot_de_passe}\"")
def step_when_remplis_formulaire_mot_de_passe(context, mot_de_passe):
    context.mot_de_passe = mot_de_passe

@when("Je soumets le formulaire d'inscription")
def step_when_soumets_formulaire_inscription(context):
    context.inscription_reussie = True


@then("Je devrais voir un message de confirmation d'inscription réussie")
def step_then_voir_message_confirmation_inscription(context):
    assert context.inscription_reussie is True, "L'inscription a échoué"


# ===== Scenario: Inscription avec email déjà utilisé =====
@given("l'utilisateur avec l'email \"{email}\" existe déjà")
def step_given_utilisateur_existe_deja(context, email):
    context.email_existant = email
    context.utilisateur_existe = True

@when("Je remplis le formulaire avec l'email : \"{email}\"")
def step_when_remplis_formulaire_email_existant(context, email):
    context.email = email
    if email == context.email_existant:
        context.inscription_reussie = False
    else:
        context.inscription_reussie = True

@then("Je devrais voir un message d'erreur indiquant que l'email est déjà utilisé")
def step_then_voir_message_erreur_email_utilise(context):
    assert context.inscription_reussie is False, "L'inscription a réussi alors que l'email est déjà utilisé"
