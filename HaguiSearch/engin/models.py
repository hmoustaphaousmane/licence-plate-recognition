from django.db import models

# Create your models here.


class Marque(models.Model):

    libele_marque = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.libele_marque

class Genre(models.Model):

    libele_genre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.libele_genre
class Declarant(models.Model):

    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    tel = models.CharField(max_length=8)
    mail = models.CharField(max_length=60)
    nni = models.IntegerField()

    def __str__(self) -> str:
        return self.nom+" "+self.prenom
    
class Engin(models.Model):
    modele = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    numero_serie = models.IntegerField()
    etat = models.BooleanField(default=False)
    numero_matricule = models.CharField(default=' ', max_length=20)
    couleur = models.CharField(max_length=50)
    source_enregie= models.CharField(max_length=50)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    declarant = models.ForeignKey(Declarant, on_delete=models.CASCADE)

    def __str__(self) -> str:

        return self.numero_serie

class Trouver(models.Model):
    engin = models.ForeignKey(Engin, on_delete=models.CASCADE)

    def __str__(self) -> str:

        return self.engin.numero_serie


