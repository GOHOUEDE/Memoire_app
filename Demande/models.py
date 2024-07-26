from django.db import models
from django.utils import  timezone
# Create your models here.
class Demande(models.Model):
    SITUATION_MATRIMONIALE_CHOICES = [
        ('C', 'Célibataire'),
        ('O', 'Marié'),
        ('S', 'Separé'),
        ('D', 'Divorcé'),
        ('V', 'Veuf'),
    ]
    STATUT_CHOICES = [
        ('rejeté', 'Rejeté'),
        ('accept', 'Accepté'),
        ('en attente', 'En attente'),
    ]

    

    SEXE_CHOICES = [
        ('Masculin', 'Masculin'),
        ('Féminin', 'Féminin'),
    ]

    PERIODICITE_REMBOURSEMENT_CHOICES = [
        ('Mensuelle', 'Mensuelle'),
        ('Bimensuelle', 'Bimensuelle'),
        ('Trimestrielle', 'Trimestrielle'),
        ('Semestrielle', 'Semestrielle'),
        ('Annuelle', 'Annuelle'),
    ]

    situation_matrimoniale = models.CharField(max_length=20, choices=SITUATION_MATRIMONIALE_CHOICES)
    profession = models.CharField(max_length=100)
    nom_prenom = models.CharField(max_length=100)
    id_agent =models.DecimalField(max_digits=10, decimal_places=2)
    age = models.PositiveIntegerField()
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES)
    anciennete_agence = models.PositiveIntegerField(help_text="En années")
    montant_solicite = models.DecimalField(max_digits=10, decimal_places=2)
    duree_pret_souhaitee = models.PositiveIntegerField(help_text="En mois")
    nombre_echeance = models.PositiveIntegerField()
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2)
    periodicite_remboursement = models.CharField(max_length=20, choices=PERIODICITE_REMBOURSEMENT_CHOICES)
    secteur_activite = models.CharField(max_length=100)
    sous_secteur_activite = models.CharField(max_length=100)
    nombre_mois_cotisation = models.PositiveIntegerField()
    statut = models.BooleanField()
    statut_traite =models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='en attente',
    )
    nbr_credits_octroyes = models.PositiveIntegerField()
    nbr_credits_rembourses = models.PositiveIntegerField()
    montant_credits_accorde = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation=models.DateTimeField(default=timezone.now)
    date_analyse=models.DateTimeField(default=timezone.now)
    date_rembouse=models.DateTimeField(default=timezone.now)
    but_demande = models.CharField(max_length=1000 ,default ="Neant")
    
    
    
