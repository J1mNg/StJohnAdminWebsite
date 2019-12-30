from django.db import models

# Create your models here.
class Reward(models.Model):
    name = models.CharField(max_length=50)
    # price = models.DecimalField(max_digits=3, decimal_places=2)
    # reward_band = models.models.IntegerField()
    # source = models.CharField(max_length=50)
