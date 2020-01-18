from django.db import models

import datetime

# Create your models here.
class Cadet(models.Model):
    user_id = models.AutoField(primary_key=True)
    dems_id = models.IntegerField(blank=False, null=False, default=0)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    years_since_joined = models.IntegerField(default=0)
    bond_paid = models.DateField(null=True, blank=True)
    joining_fee_paid = models.DateField(null=True, blank=True)
    rank = models.CharField(max_length=50, null=True, blank=True)
    qualification = models.CharField(max_length=50, null=True, blank=True)
    total_duty_hours = models.DecimalField(default=0, max_digits = 7, decimal_places = 2)
    num_of_events = models.IntegerField(default=0)
    training_hours = models.DecimalField(default=0, max_digits = 7, decimal_places = 2)
    other_hours = models.DecimalField(default=0, max_digits = 7, decimal_places = 2)
    meeting_hours = models.DecimalField(default=0, max_digits = 7, decimal_places = 2)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.firstname + " " + self.lastname
