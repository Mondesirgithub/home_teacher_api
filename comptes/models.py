from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class Utilisateur(AbstractUser):
    # Attributs communs à tous les types d'utilisateurs
    telephone1 = models.CharField(max_length=30,null=True, blank=True,unique=True)
    telephone2 = models.CharField(max_length=30, null=True, blank=True,unique=True)

    class Meta:
        # Définit la table dans la base de données pour la classe parente Utilisateur
        db_table = 'utilisateur'

class Tuteur(Utilisateur):
    # Attributs spécifiques au tuteur
    profession = models.CharField(max_length=50)

    class Meta:
        # Définit la table dans la base de données pour la classe Tuteur
        db_table = 'tuteur'
    
    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"

class Eleve(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()
    classe = models.CharField(max_length=50)
    ecole = models.CharField(max_length=50)
    periode_journee = models.CharField(max_length=50)
    jours_disponibles = models.CharField(max_length=50)
    difficulte = models.TextField()
    lieu_travail = models.CharField(max_length=50)
    idtuteur = models.ForeignKey(Tuteur, on_delete=models.CASCADE, verbose_name='tuteur', null=True,blank=True)


    def __str__(self) -> str:
        return f"{self.nom} {self.prenom}"
    
    def save(self, *args, **kwargs):
        if "/" in self.date_naissance:
            day, month, year = self.date_naissance.split('/') # Récupération de la journée, du mois et de l'année
        else:
            day, month, year = self.date_naissance.split('-') # Récupération de la journée, du mois et de l'année
        my_date = date(int(day), int(month), int(year)) # Conversion de la date au format souhaité
        self.date_naissance = my_date
        super(Eleve, self).save(*args, **kwargs)

class Professeur(Utilisateur):
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=50)
    statut = models.CharField(max_length=30)
    #--Statut Etudiant
    universite = models.CharField(max_length=30, null=True, blank=True)
    filiere_etude = models.CharField(max_length=30, null=True, blank=True)
    annee_etude = models.CharField(max_length=30, null=True, blank=True)
    #---Statut Enseignant
    dernier_diplome = models.CharField(max_length=100, null=True, blank=True)
    filiere_dernier_diplome = models.CharField(max_length=100,blank=True, null=True)
    #--special encadrement
    jours_disponibles = models.CharField(max_length=100)
    matieres_generales_enseignables = models.CharField(max_length=100,blank=True, null=True)
    classes_generales_enseignables = models.CharField(max_length=100,blank=True, null=True)
    classes_techniques_enseignables = models.CharField(max_length=100, blank=True, null=True)
    matieres_techniques_enseignables = models.CharField(max_length=100, blank=True, null=True)
    zones_travail = models.CharField(max_length=100)
    periode_journee = models.CharField(max_length=50)
    piece_jointe = models.FileField(upload_to="piece_jointes/")
    ideleves = models.ManyToManyField(Eleve, through='Encadrement', verbose_name='eleves')


    class Meta:
        # Définit la table dans la base de données pour la classe Professeur
        db_table = 'professeur'
    
    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"



class Encadrement(models.Model):
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self) -> str:
        return f"Prof : {self.professeur.last_name} {self.professeur.first_name} - Eleve : {self.eleve.nom} {self.eleve.prenom}"