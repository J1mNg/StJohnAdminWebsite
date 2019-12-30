from django.db import models

import datetime

# Create your models here.
class Cadet(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    years_since_joined = models.IntegerField(null=True, blank=True)
    bond_paid = models.DateField(null=True, blank=True)
    joining_fee_paid = models.DateField(null=True, blank=True)
    rank = models.CharField(max_length=50, null=True, blank=True)
    qualification = models.CharField(max_length=50, null=True, blank=True)
    total_duty_hours = models.IntegerField(null=True, blank=True)
    num_of_events = models.IntegerField(null=True, blank=True)
    training_hours = models.IntegerField(null=True, blank=True)
    other_hours = models.IntegerField(null=True, blank=True)
    meeting_hours = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.firstname + " " + self.lastname