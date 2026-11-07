from django.urls import path
from formations import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('formations/', views.liste_formations, name='liste_formations'),
    path(
        'formations/<int:id>/inscrire/',
        views.inscrire_formation,
        name='inscrire_formation'
    ),
    path('formations/ajouter/', views.ajouter_formation, name='ajouter_formation'),
    path('formations/<int:id>/modifier/', views.modifier_formation, name='modifier_formation'),
    path('formations/<int:id>/supprimer/',  views.supprimer_formation, name='supprimer_formation'),
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/<int:etudiant_id>/', views.detail_etudiant, name='detail_etudiant'),
    path(
        'inscription/',
        views.inscription_etudiant,
        name='inscription_etudiant'
    ),
    path(
        'mon-profil/',
        views.mon_profil,
        name='mon_profil'
    ),
    path(
        'mon-profil/modifier/',
        views.modifier_mon_profil,
        name='modifier_mon_profil'
    ),
    path(
        'mon-profil/changer-mot-de-passe/',
        views.changer_mot_de_passe,
        name='changer_mot_de_passe'
    ),
    path(
        'apres-connexion/',
        views.redirection_apres_connexion,
        name='redirection_apres_connexion'
    ),
    path(
        'inscriptions/',
        views.liste_inscriptions,
        name='liste_inscriptions'
    ),
    path(
        'inscriptions/<int:id>/valider/',
        views.valider_inscription,
        name='valider_inscription'
    ),
    path(
        'inscriptions/<int:id>/annuler/',
        views.annuler_inscription,
        name='annuler_inscription'
    ),
    path(
        'tableau-de-bord/',
        views.tableau_de_bord,
        name='tableau_de_bord'
    ),

]