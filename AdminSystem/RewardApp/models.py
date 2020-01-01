from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from CadetApp.models import Cadet

# Create your models here.
class Reward_Band(models.Model):
    id = models.AutoField(primary_key=True)
    reward_band = models.IntegerField(null=True, blank=False)
    required_points = models.PositiveIntegerField(null=True, blank=False)

    def __str__(self):
        return "Band {}: Points Required - {}".format(self.reward_band, self.required_points)

class Reward(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0.00)])
    required_points = models.ForeignKey(Reward_Band, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=50, default="unknown")
    link = models.CharField(max_length=100, default="Not Applicable")
    comments = models.CharField(max_length=246, blank=True, null=True)
    IsActive = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class User_Reward_Log(models.Model):
    id = models.AutoField(primary_key=True)
    cadet = models.ForeignKey(Cadet, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    reward_claim_date = models.DateField(null=True)

    def __str__(self):
        return "Cadet {}: Reward - {} ({})".format(self.cadet, self.reward, self.reward_claim_date)