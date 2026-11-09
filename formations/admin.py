
from django.contrib import admin
from .models import Formation, Etudiant, Inscription


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'duree_semaines', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('nom',)


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone')
    search_fields = ('nom', 'prenom', 'email')


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'etudiant',
        'formation',
        'statut',
        'date_inscription'
    )
    list_filter = ('statut',)
    search_fields = (
        'etudiant__nom',
        'etudiant__prenom',
        'formation__nom'
    )
