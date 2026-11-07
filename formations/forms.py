
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import models

from .models import Formation, Etudiant

User = get_user_model()



class FormationForm(forms.ModelForm):

    class Meta:
        model = Formation
        fields = [
            'nom',
            'description',
            'duree_semaines',
            'prix',
            'disponible',
            'image',
        ]

        labels = {
            'nom': 'Nom de la formation',
            'description': 'Description',
            'duree_semaines': 'Durée (en semaines)',
            'prix': 'Prix (FCFA)',
            'disponible': 'Formation disponible',
            'image': 'Image de la formation',
        }

        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex. : Développement web avec Python',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez le contenu de la formation...',
                'rows': 4,
            }),
            'duree_semaines': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }



class InscriptionEtudiantForm(UserCreationForm):
    nom = forms.CharField(
        max_length=100,
        label="Nom"
    )
    prenom = forms.CharField(
        max_length=100,
        label="Prénom"
    )
    email = forms.EmailField(
        label="Adresse e-mail"
    )
    telephone = forms.CharField(
        max_length=20,
        required=False,
        label="Téléphone"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
        )

    def clean_email(self):
        email = self.cleaned_data['email'].strip()

        # Vérifier les fiches étudiants existantes
        if Etudiant.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "Cette adresse e-mail est déjà associée à un étudiant."
            )

        # Vérifier les comptes Django existants
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "Cette adresse e-mail est déjà utilisée par un compte."
            )

        return email



class EtudiantProfilForm(forms.ModelForm):

    class Meta:
        model = Etudiant
        fields = [
            'nom',
            'prenom',
            'telephone',
        ]

        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'telephone': 'Téléphone',
        }

        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom',
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre numéro de téléphone',
            }),
        }
