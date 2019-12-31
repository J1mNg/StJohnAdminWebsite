from django.db import models
from CadetApp.models import Cadet

# Create your models here.

class Meeting(models.Model):
    TERM_CHOICES = [
        (1, 'Term 1'),
        (2, 'Term 2'),
        (3, 'Term 3'),
        (4, 'Term 4'),
    ]
    term = models.IntegerField(choices=TERM_CHOICES,)
    date = models.DateField(unique=True)

    def __str__(self):
        return "term " + str(self.term) + " " + str(self.date)

class Meeting_Cadet(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    cadet = models.ForeignKey(Cadet, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Attendance(Meeting_Cadet):
    uniform = models.BooleanField()

    def __str__(self):
        return str(self.cadet) + " " + str(self.meeting)

class Absence(Meeting_Cadet):
    REASON_CODES = [
        ('u', 'Unexplained'),
        ('e', 'Exams'),
        ('r', 'Religious Leave'),
        ('o', 'Other'),
    ]
    reason_code = models.CharField(max_length=1,choices=REASON_CODES, default='o')

    def __str__(self):
        return str(self.cadet) + " " + str(self.meeting)
