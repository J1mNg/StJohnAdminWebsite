from django.db import models

# Create your models here.
class CadetsList(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)