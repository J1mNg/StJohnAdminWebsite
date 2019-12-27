from django.db import models

import datetime

# Create your models here.
class Cadet(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, default="null")
    lastname = models.CharField(max_length=50, default="null")
    birthday = models.DateField(null=True)
    age = models.IntegerField(default=0, null=True)
    mobile = models.IntegerField(default=0, null=True)
    email = models.EmailField(max_length=254, default='default@example.com', null=True)
    date_joined = models.DateField(null=True)
    years_since_joined = models.IntegerField(default=0, null=True)
    bond_paid = models.DateField(null=True)
    joining_fee_paid = models.DateField(null=True)
    rank = models.CharField(max_length=50, null=True)
    qualification = models.CharField(max_length=50, default="null", null=True)
    total_duty_hours = models.IntegerField(default=0, null=True)
    num_of_events = models.IntegerField(default=0, null=True)
    training_hours = models.IntegerField(default=0, null=True)
    other_hours = models.IntegerField(default=0,null=True)
    meeting_hours = models.IntegerField(default=0, null=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.firstname + " " + self.lastname