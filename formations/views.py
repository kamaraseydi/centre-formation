
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core.paginator import Paginator
from . import models
from .models import Formation, Etudiant, Inscription
from django.db import transaction
from django.contrib.auth import login
from .forms import FormationForm, InscriptionEtudiantForm, EtudiantProfilForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
# Create your views here.

def accueil(request):
    formations = Formation.objects.all()
    contexte = {
        'nom_centre': 'Centre de Formation Seydi',
        'nombre_formations': formations.count(),
        'annee_creation': 2026,
        'inscriptions_ouvertes': True
    }
    return render(request, 'formations/accueil.html',contexte)



def liste_formations(request):
    recherche = request.GET.get('q', '')
    disponibles_seulement = request.GET.get('disponibles') == 'oui'

    formations = Formation.objects.all()

    if recherche:
        formations = formations.filter(
            nom__icontains=recherche
        )

    if disponibles_seulement:
        formations = formations.filter(disponible=True)

    contexte = {
        'formations': formations,
        'recherche': recherche,
        'disponibles_seulement': disponibles_seulement,
    }

    return render(request,'formations/formations.html',contexte)


@permission_required('formations.add_formation', raise_exception=True)
def ajouter_formation(request):
    if request.method == 'POST':
        formulaire = FormationForm(
            request.POST,
            request.FILES
        )

        if formulaire.is_valid():
            formulaire.save()
            return redirect('liste_formations')

    else:
        formulaire = FormationForm()

    contexte = {
        'formulaire': formulaire,
    }

    return render(
        request,
        'formations/ajouter_formation.html',
        contexte
    )


@permission_required('formations.change_formation', raise_exception=True)
def modifier_formation(request, id):
    formation = get_object_or_404(Formation, id=id)

    if request.method == 'POST':
        formulaire = FormationForm(
            request.POST,
            request.FILES,
            instance=formation
        )

        if formulaire.is_valid():
            formulaire.save()
            return redirect('liste_formations')

    else:
        formulaire = FormationForm(instance=formation)

    contexte = {
        'formulaire': formulaire,
        'formation': formation,
    }

    return render(
        request,
        'formations/modifier_formation.html',
        contexte
    )


@permission_required('formations.delete_formation', raise_exception=True)
def supprimer_formation(request, id):
    formation = get_object_or_404(Formation, id=id)

    if request.method == 'POST':
        formation.delete()
        return redirect('liste_formations')

    contexte = {
        'formation': formation,
    }

    return render(request,'formations/confirmer_suppression.html',contexte)

@permission_required('formations.view_etudiant',raise_exception=True)
def liste_etudiants(request):
    etudiants = Etudiant.objects.prefetch_related(
        'inscriptions__formation'
    ).order_by('nom', 'prenom')

    contexte = {
        'etudiants': etudiants,
    }

    return render(request, 'formations/etudiants.html', contexte)


@permission_required('formations.view_etudiant',raise_exception=True)
def detail_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(
        Etudiant.objects.prefetch_related(
            'inscriptions__formation'
        ),
        id=etudiant_id
    )

    contexte = {
        'etudiant': etudiant,
        'inscriptions': etudiant.inscriptions.all(),
    }

    return render(request,'formations/detail_etudiant.html',contexte)



@login_required
@require_POST
def inscrire_formation(request, id):
    formation = get_object_or_404(Formation, id=id)

    # Vérifier que la formation est disponible
    if not formation.disponible:
        messages.error(
            request,
            "Les inscriptions à cette formation sont fermées."
        )
        return redirect('liste_formations')

    # Vérifier que le compte possède une fiche étudiant
    try:
        etudiant = request.user.profil_etudiant
    except Etudiant.DoesNotExist:
        messages.error(
            request,
            "Aucune fiche étudiant n'est associée à votre compte."
        )
        return redirect('liste_formations')

    # Empêcher les inscriptions en double
    try:
        with transaction.atomic():
            Inscription.objects.create(
                etudiant=etudiant,
                formation=formation,
                statut='EN_ATTENTE'
            )

    except IntegrityError:
        messages.warning(
            request,
            "Vous êtes déjà inscrit à cette formation."
        )
        return redirect('mon_profil')

    messages.success(
        request,
        f"Votre demande d'inscription à {formation.nom} a été enregistrée."
    )

    return redirect('mon_profil')



@login_required
def mon_profil(request):
    etudiant = get_object_or_404(
        Etudiant.objects.prefetch_related(
            'inscriptions__formation'
        ),
        user=request.user
    )

    contexte = {
        'etudiant': etudiant,
        'inscriptions': etudiant.inscriptions.all(),
    }

    return render(
        request,
        'formations/mon_profil.html',
        contexte
    )


@login_required
def modifier_mon_profil(request):
    etudiant = get_object_or_404(
        Etudiant,
        user=request.user
    )

    if request.method == 'POST':
        formulaire = EtudiantProfilForm(
            request.POST,
            instance=etudiant
        )

        if formulaire.is_valid():
            formulaire.save()

            messages.success(
                request,
                "Votre profil a été modifié avec succès."
            )

            return redirect('mon_profil')

    else:
        formulaire = EtudiantProfilForm(
            instance=etudiant
        )

    contexte = {
        'formulaire': formulaire,
        'etudiant': etudiant,
    }

    return render(
        request,
        'formations/modifier_mon_profil.html',
        contexte
    )


@login_required
def changer_mot_de_passe(request):
    if request.method == 'POST':
        formulaire = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if formulaire.is_valid():
            utilisateur = formulaire.save()

            # Maintenir la session après le changement du mot de passe
            update_session_auth_hash(request, utilisateur)

            messages.success(
                request,
                "Votre mot de passe a été modifié avec succès."
            )

            return redirect('mon_profil')

    else:
        formulaire = PasswordChangeForm(
            user=request.user
        )

    contexte = {
        'formulaire': formulaire,
    }

    return render(
        request,
        'formations/changer_mot_de_passe.html',
        contexte
    )

@login_required
def redirection_apres_connexion(request):
    try:
        request.user.profil_etudiant
    except Etudiant.DoesNotExist:
        return redirect('accueil')

    return redirect('mon_profil')



@permission_required('formations.view_inscription', raise_exception=True)
def liste_inscriptions(request):
    inscriptions = Inscription.objects.select_related(
        'etudiant',
        'formation'
    ).order_by('-date_inscription', '-id')

    # 1. Récupérer les critères de recherche
    recherche = request.GET.get('q', '').strip()
    statut = request.GET.get('statut', '').strip()

    # 2. Rechercher un étudiant par nom, prénom ou e-mail
    if recherche:
        inscriptions = inscriptions.filter(
            Q(etudiant__nom__icontains=recherche)
            | Q(etudiant__prenom__icontains=recherche)
            | Q(etudiant__email__icontains=recherche)
        )

    # 3. Filtrer par statut
    statuts_valides = [
        choix[0] for choix in Inscription.STATUT_CHOICES
    ]

    if statut in statuts_valides:
        inscriptions = inscriptions.filter(statut=statut)
    else:
        statut = ''

    # 4. Diviser les résultats en pages de 10 inscriptions
    paginator = Paginator(inscriptions, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    contexte = {
        'inscriptions': page_obj,
        'page_obj': page_obj,
        'recherche': recherche,
        'statut_selectionne': statut,
    }

    return render(
        request,
        'formations/inscriptions.html',
        contexte
    )


@permission_required('formations.change_inscription', raise_exception=True)
@require_POST
def valider_inscription(request, id):
    inscription = get_object_or_404(Inscription, id=id)

    if inscription.statut != 'EN_ATTENTE':
        messages.warning(
            request,
            "Cette inscription n'est plus en attente."
        )
    else:
        inscription.statut = 'VALIDEE'
        inscription.save(update_fields=['statut'])
        messages.success(request, "Inscription validée avec succès.")

    return redirect('liste_inscriptions')


@permission_required('formations.change_inscription', raise_exception=True)
@require_POST
def annuler_inscription(request, id):
    inscription = get_object_or_404(Inscription, id=id)

    if inscription.statut != 'EN_ATTENTE':
        messages.warning(
            request,
            "Cette inscription n'est plus en attente."
        )
    else:
        inscription.statut = 'ANNULEE'
        inscription.save(update_fields=['statut'])
        messages.success(request, "Inscription annulée avec succès.")

    return redirect('liste_inscriptions')



@permission_required('formations.view_inscription', raise_exception=True)
def tableau_de_bord(request):
    contexte = {
        'nombre_formations': Formation.objects.count(),
        'nombre_etudiants': Etudiant.objects.count(),

        'inscriptions_en_attente': Inscription.objects.filter(
            statut='EN_ATTENTE'
        ).count(),

        'inscriptions_validees': Inscription.objects.filter(
            statut='VALIDEE'
        ).count(),

        'inscriptions_annulees': Inscription.objects.filter(
            statut='ANNULEE'
        ).count(),

        'inscriptions_recentes': Inscription.objects.select_related(
            'etudiant', 'formation'
        ).order_by('-date_inscription', '-id')[:5],
    }

    return render(
        request,
        'formations/tableau_de_bord.html',
        contexte
    )

def inscription_etudiant(request):
    # Un utilisateur déjà connecté ne crée pas un second compte ici.
    if request.user.is_authenticated:
        return redirect('accueil')

    if request.method == 'POST':
        formulaire = InscriptionEtudiantForm(request.POST)

        if formulaire.is_valid():
            with transaction.atomic():
                # Création du compte Django
                utilisateur = formulaire.save(commit=False)
                utilisateur.email = formulaire.cleaned_data['email']
                utilisateur.save()

                # Création de la fiche étudiant liée au compte
                Etudiant.objects.create(
                    user=utilisateur,
                    nom=formulaire.cleaned_data['nom'],
                    prenom=formulaire.cleaned_data['prenom'],
                    email=formulaire.cleaned_data['email'],
                    telephone=formulaire.cleaned_data['telephone'],
                )

            # Connecter automatiquement l'étudiant
            login(request, utilisateur)

            return redirect('mon_profil')

    else:
        formulaire = InscriptionEtudiantForm()

    contexte = {
        'formulaire': formulaire,
    }

    return render(
        request,
        'formations/inscription_etudiant.html',
        contexte
    )