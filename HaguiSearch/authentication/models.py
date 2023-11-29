from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Utilisateur(AbstractUser):
    poste = models.TextField(blank=True)

    def __str__(self):
        return self.username

