from django.db import models

# Create your models here.
class Cadet(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)

    def __str__(self):
        return self.firstName + " " + self.lastName