from django.test import TestCase

# Create your tests here.

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import IntegrityError, transaction

from .models import Formation, Etudiant, Inscription
from .forms import (
    FormationForm,
    InscriptionEtudiantForm,
    EtudiantProfilForm,
)

User = get_user_model()


# ==========================================================
# DONNEES DE BASE UTILISEES PAR LES TESTS
# ==========================================================

class BaseTestCase(TestCase):

    def setUp(self):
        self.formation = Formation.objects.create(
            nom="Développement Python",
            description="Apprentissage de Python et Django",
            duree_semaines=12,
            prix=Decimal("75000.00"),
            disponible=True,
        )

        self.user = User.objects.create_user(
            username="etudiant_test",
            email="etudiant@test.com",
            password="TestPassword!2026",
        )

        self.etudiant = Etudiant.objects.create(
            nom="Kamara",
            prenom="Seydi",
            email="etudiant@test.com",
            telephone="770000000",
            user=self.user,
        )

        self.inscription = Inscription.objects.create(
            etudiant=self.etudiant,
            formation=self.formation,
        )

        # Utilisateur disposant de toutes les permissions
        # de l'application formations.
        self.staff = User.objects.create_user(
            username="gestionnaire",
            password="TestPassword!2026",
        )

        permissions = Permission.objects.filter(
            content_type__app_label="formations"
        )

        self.staff.user_permissions.add(*permissions)


# ==========================================================
# 1. TESTS DES MODELES
# ==========================================================

class FormationModelTests(BaseTestCase):

    def test_creation_formation(self):
        self.assertEqual(self.formation.nom, "Développement Python")
        self.assertEqual(self.formation.prix, Decimal("75000.00"))
        self.assertTrue(self.formation.disponible)

    def test_str_formation(self):
        self.assertEqual(
            str(self.formation),
            "Développement Python"
        )


class EtudiantModelTests(BaseTestCase):

    def test_creation_etudiant(self):
        self.assertEqual(self.etudiant.nom, "Kamara")
        self.assertEqual(self.etudiant.prenom, "Seydi")
        self.assertEqual(self.etudiant.user, self.user)

    def test_str_etudiant(self):
        self.assertEqual(str(self.etudiant), "Seydi Kamara")


class InscriptionModelTests(BaseTestCase):

    def test_creation_inscription(self):
        self.assertEqual(
            self.inscription.statut,
            "EN_ATTENTE"
        )

    def test_str_inscription(self):
        self.assertEqual(
            str(self.inscription),
            "Seydi Kamara - Développement Python"
        )

    def test_doublon_inscription_interdit(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Inscription.objects.create(
                    etudiant=self.etudiant,
                    formation=self.formation,
                )


# ==========================================================
# 2. TESTS DES FORMULAIRES
# ==========================================================

class FormationFormTests(TestCase):

    def donnees_valides(self):
        return {
            "nom": "Formation Django",
            "description": "Apprendre Django",
            "duree_semaines": 8,
            "prix": "50000.00",
            "disponible": "on",
        }

    def test_formulaire_formation_valide(self):
        formulaire = FormationForm(
            data=self.donnees_valides()
        )

        self.assertTrue(formulaire.is_valid())

    def test_duree_inferieure_a_un_refusee(self):
        donnees = self.donnees_valides()
        donnees["duree_semaines"] = 0

        formulaire = FormationForm(data=donnees)

        self.assertFalse(formulaire.is_valid())

    def test_prix_negatif_refuse(self):
        donnees = self.donnees_valides()
        donnees["prix"] = "-100"

        formulaire = FormationForm(data=donnees)

        self.assertFalse(formulaire.is_valid())


class InscriptionEtudiantFormTests(BaseTestCase):

    def donnees_valides(self):
        return {
            "username": "nouvel_etudiant",
            "nom": "Diop",
            "prenom": "Moussa",
            "email": "moussa@test.com",
            "telephone": "771234567",
            "password1": "S3cur3!Passw0rd-XYZ",
            "password2": "S3cur3!Passw0rd-XYZ",
        }

    def test_formulaire_inscription_valide(self):
        formulaire = InscriptionEtudiantForm(
            data=self.donnees_valides()
        )

        self.assertTrue(formulaire.is_valid())

    def test_email_etudiant_deja_utilise_refuse(self):
        donnees = self.donnees_valides()
        donnees["email"] = self.etudiant.email

        formulaire = InscriptionEtudiantForm(data=donnees)

        self.assertFalse(formulaire.is_valid())
        self.assertIn("email", formulaire.errors)

    def test_email_compte_deja_utilise_refuse(self):
        donnees = self.donnees_valides()
        donnees["email"] = "gestionnaire@test.com"

        User.objects.filter(username="gestionnaire").update(
            email="gestionnaire@test.com"
        )

        formulaire = InscriptionEtudiantForm(data=donnees)

        self.assertFalse(formulaire.is_valid())
        self.assertIn("email", formulaire.errors)


class EtudiantProfilFormTests(BaseTestCase):

    def test_modification_profil_valide(self):
        formulaire = EtudiantProfilForm(
            data={
                "nom": "Fall",
                "prenom": "Moussa",
                "telephone": "780000000",
            },
            instance=self.etudiant,
        )

        self.assertTrue(formulaire.is_valid())

        profil = formulaire.save()

        self.assertEqual(profil.nom, "Fall")
        self.assertEqual(profil.prenom, "Moussa")


# ==========================================================
# 3. TESTS DES PAGES PUBLIQUES ET DES FORMATIONS
# ==========================================================

class FormationViewsTests(BaseTestCase):

    def test_accueil_accessible(self):
        response = self.client.get(reverse("accueil"))

        self.assertEqual(response.status_code, 200)

    def test_liste_formations_accessible(self):
        response = self.client.get(
            reverse("liste_formations")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.formation.nom)

    def test_recherche_formation(self):
        response = self.client.get(
            reverse("liste_formations"),
            {"q": "Python"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Développement Python")

    def test_filtre_formations_disponibles(self):
        Formation.objects.create(
            nom="Formation fermée",
            description="Formation indisponible",
            duree_semaines=4,
            prix=Decimal("25000.00"),
            disponible=False,
        )

        response = self.client.get(
            reverse("liste_formations"),
            {"disponibles": "oui"},
        )

        self.assertContains(response, "Développement Python")
        self.assertNotContains(response, "Formation fermée")

    def test_ajout_formation_sans_permission_refuse(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("ajouter_formation")
        )

        self.assertEqual(response.status_code, 403)

    def test_ajout_formation_avec_permission(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse("ajouter_formation"),
            {
                "nom": "Java Spring Boot",
                "description": "Formation backend Java",
                "duree_semaines": 10,
                "prix": "90000.00",
                "disponible": "on",
            },
        )

        self.assertRedirects(
            response,
            reverse("liste_formations"),
        )

        self.assertTrue(
            Formation.objects.filter(
                nom="Java Spring Boot"
            ).exists()
        )

    def test_modification_formation(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "modifier_formation",
                args=[self.formation.id],
            ),
            {
                "nom": "Python avancé",
                "description": "Formation avancée",
                "duree_semaines": 15,
                "prix": "85000.00",
                "disponible": "on",
            },
        )

        self.assertRedirects(
            response,
            reverse("liste_formations"),
        )

        self.formation.refresh_from_db()

        self.assertEqual(
            self.formation.nom,
            "Python avancé",
        )

    def test_suppression_formation(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "supprimer_formation",
                args=[self.formation.id],
            )
        )

        self.assertRedirects(
            response,
            reverse("liste_formations"),
        )

        self.assertFalse(
            Formation.objects.filter(
                id=self.formation.id
            ).exists()
        )


# ==========================================================
# 4. TESTS DE L'AUTHENTIFICATION ET DU PROFIL
# ==========================================================

class AuthenticationViewsTests(BaseTestCase):

    def test_profil_etudiant_demande_connexion(self):
        response = self.client.get(
            reverse("mon_profil")
        )

        self.assertEqual(response.status_code, 302)

    def test_profil_etudiant_connecte(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("mon_profil")
        )

        self.assertEqual(response.status_code, 200)

    def test_inscription_nouvel_etudiant(self):
        response = self.client.post(
            reverse("inscription_etudiant"),
            {
                "username": "nouveau_compte",
                "nom": "Ndiaye",
                "prenom": "Awa",
                "email": "awa@test.com",
                "telephone": "760000000",
                "password1": "S3cur3!Passw0rd-XYZ",
                "password2": "S3cur3!Passw0rd-XYZ",
            },
        )

        self.assertRedirects(
            response,
            reverse("mon_profil"),
        )

        nouvel_utilisateur = User.objects.get(
            username="nouveau_compte"
        )

        self.assertTrue(
            Etudiant.objects.filter(
                user=nouvel_utilisateur
            ).exists()
        )

        self.assertTrue(
            self.client.session.get("_auth_user_id")
        )

    def test_compte_connecte_ne_peut_pas_creer_un_second_compte(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("inscription_etudiant")
        )

        self.assertRedirects(
            response,
            reverse("accueil"),
        )

    def test_modification_profil(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("modifier_mon_profil"),
            {
                "nom": "Sarr",
                "prenom": "Alioune",
                "telephone": "770000001",
            },
        )

        self.assertRedirects(
            response,
            reverse("mon_profil"),
        )

        self.etudiant.refresh_from_db()

        self.assertEqual(self.etudiant.nom, "Sarr")

    def test_changement_mot_de_passe(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("changer_mot_de_passe"),
            {
                "old_password": "TestPassword!2026",
                "new_password1": "NewPassword!2026",
                "new_password2": "NewPassword!2026",
            },
        )

        self.assertRedirects(
            response,
            reverse("mon_profil"),
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password("NewPassword!2026")
        )


# ==========================================================
# 5. TESTS DES INSCRIPTIONS AUX FORMATIONS
# ==========================================================

class InscriptionViewsTests(BaseTestCase):

    def test_inscription_necessite_une_connexion(self):
        response = self.client.post(
            reverse(
                "inscrire_formation",
                args=[self.formation.id],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Inscription.objects.count(), 1)

    def test_inscription_formation_reussie(self):
        self.client.force_login(self.user)

        autre_formation = Formation.objects.create(
            nom="Java",
            description="Apprendre Java",
            duree_semaines=10,
            prix=Decimal("60000.00"),
            disponible=True,
        )

        response = self.client.post(
            reverse(
                "inscrire_formation",
                args=[autre_formation.id],
            )
        )

        self.assertRedirects(
            response,
            reverse("mon_profil"),
        )

        self.assertTrue(
            Inscription.objects.filter(
                etudiant=self.etudiant,
                formation=autre_formation,
            ).exists()
        )

    def test_doublon_inscription_refuse(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "inscrire_formation",
                args=[self.formation.id],
            )
        )

        self.assertRedirects(
            response,
            reverse("mon_profil"),
        )

        self.assertEqual(Inscription.objects.count(), 1)

    def test_formation_indisponible_refuse_inscription(self):
        self.client.force_login(self.user)

        formation_fermee = Formation.objects.create(
            nom="Formation fermée",
            description="Inscriptions fermées",
            duree_semaines=6,
            prix=Decimal("30000.00"),
            disponible=False,
        )

        response = self.client.post(
            reverse(
                "inscrire_formation",
                args=[formation_fermee.id],
            )
        )

        self.assertRedirects(
            response,
            reverse("liste_formations"),
        )

        self.assertFalse(
            Inscription.objects.filter(
                formation=formation_fermee
            ).exists()
        )

    def test_validation_inscription(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "valider_inscription",
                args=[self.inscription.id],
            )
        )

        self.assertRedirects(
            response,
            reverse("liste_inscriptions"),
        )

        self.inscription.refresh_from_db()

        self.assertEqual(
            self.inscription.statut,
            "VALIDEE",
        )

    def test_annulation_inscription(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "annuler_inscription",
                args=[self.inscription.id],
            )
        )

        self.assertRedirects(
            response,
            reverse("liste_inscriptions"),
        )

        self.inscription.refresh_from_db()

        self.assertEqual(
            self.inscription.statut,
            "ANNULEE",
        )

    def test_validation_inscription_refusee_en_get(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse(
                "valider_inscription",
                args=[self.inscription.id],
            )
        )

        self.assertEqual(response.status_code, 405)

        self.inscription.refresh_from_db()

        self.assertEqual(
            self.inscription.statut,
            "EN_ATTENTE",
        )


# ==========================================================
# 6. TESTS DES PERMISSIONS ET DE L'ADMINISTRATION METIER
# ==========================================================

class PermissionViewsTests(BaseTestCase):

    def test_etudiant_ne_peut_pas_voir_liste_etudiants(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("liste_etudiants")
        )

        self.assertEqual(response.status_code, 403)

    def test_gestionnaire_peut_voir_liste_etudiants(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("liste_etudiants")
        )

        self.assertEqual(response.status_code, 200)

    def test_gestionnaire_peut_voir_detail_etudiant(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse(
                "detail_etudiant",
                args=[self.etudiant.id],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_liste_inscriptions_accessible_au_gestionnaire(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("liste_inscriptions")
        )

        self.assertEqual(response.status_code, 200)

    def test_recherche_inscriptions(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("liste_inscriptions"),
            {"q": "Seydi"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seydi")

    def test_filtre_inscriptions_par_statut(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("liste_inscriptions"),
            {"statut": "EN_ATTENTE"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "EN_ATTENTE")

    def test_tableau_de_bord_accessible_au_gestionnaire(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("tableau_de_bord")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["nombre_formations"],
            1,
        )
        self.assertEqual(
            response.context["nombre_etudiants"],
            1,
        )
        self.assertEqual(
            response.context["inscriptions_en_attente"],
            1,
        )
