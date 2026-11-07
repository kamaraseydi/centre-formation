from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class Formation(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField()
    duree_semaines = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    disponible = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to='formations/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nom




class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profil_etudiant'
    )

    def __str__(self):
        return f"{self.prenom} {self.nom}"



class Inscription(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('ANNULEE', 'Annulée'),
    ]

    etudiant = models.ForeignKey(
        Etudiant,
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )

    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )

    date_inscription = models.DateField(auto_now_add=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['etudiant', 'formation'],
                name='unique_inscription_etudiant_formation'
            )
        ]

    def __str__(self):
        return f"{self.etudiant} - {self.formation}"

