from django.db import models

import datetime

# Create your models here.
class Cadet(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, default="null")
    lastname = models.CharField(max_length=50, default="null")
    birthday = models.DateField(null=True)
    age = models.IntegerField(default=0)
    mobile = models.IntegerField(default=0)
    email = models.EmailField(max_length=254, default='default@example.com')
    date_joined = models.DateField(null=True)
    years_since_joined = models.IntegerField(default=0)
    bond_paid = models.DateField(null=True)
    joining_fee_paid = models.DateField(null=True)
    rank = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50, default="null")
    total_duty_hours = models.IntegerField(default=0)
    num_of_events = models.IntegerField(default=0)
    training_hours = models.IntegerField(default=0)
    other_hours = models.IntegerField(default=0)
    meeting_hours = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.firstname + " " + self.lastname