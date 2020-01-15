from django.db import models
from django.core.exceptions import ValidationError
from CadetApp.models import Cadet
from RollMarkingApp.models import Meeting_Cadet, Meeting
from django.db.models import Avg, Count, Min, Sum
# Create your models here.

# inherits from Meeting_Cadet (Abstract Model --> placeholder model to include those fields here)
class TermFee(Meeting_Cadet):
    amount = models.IntegerField()

    # we can redefine methods here --> provides row-based functionality

    # string representation when model instance needs to be displayed
    # for example, when selecting an instance as ForeignKey in a form
    def __str__(self):
        return str(self.cadet) + " " + str(self.meeting) + " paid"

    #when validating a model --> validate
        # 1. model's fields  --> Model.clean_fields()
        # 2. model as a whole  --> Model.clean()
        # 3. uniqueness constraints --> Model.validate_unique()

    # we redefine validation of uniqueness to include
    # the fact that each cadet can only pay TermFees once per term.

    # validate_unique is automatically called in save() method
    def validate_unique(self, exclude=None):
        # instance --> a row for table
        # self.meeting.term --> get the instance we entered into form and see what is the term field

        # cadet=self.cadet --> retrieve all TermFee objects for the cadet we entered into form (see what payments they've made)
        # meeting__term=self.meeting.term --> check what term they've made a payment in
        # if the term we entered in is same as the terms above --> i.e. if we are able to filter for these results and it exists
        # raise validation error
        if TermFee.objects.filter(cadet=self.cadet, meeting__term=self.meeting.term).exists():
            raise ValidationError('Cadet has already paid Term Fee for this term')

    class Meta:
        unique_together = ('meeting', 'cadet',)

class OtherIncome(Meeting_Cadet):
    amount = models.IntegerField()
    details = models.TextField(max_length=100)

    def __str__(self):
        return str(self.cadet) + " " + str(self.meeting) + " other income " + str(self.amount)

class Expense(Meeting_Cadet):
    amount = models.IntegerField()
    details = models.TextField(max_length=100)

    def __str__(self):
        return str(self.cadet) + " " + str(self.meeting) + " expense " + str(self.amount)

class CashBox(models.Model):
    amount = models.IntegerField()
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    deficit = models.IntegerField(default=0)

    def current_amount(self):
            cashbox_current = self.amount
            latest_cashbox_date = self.meeting.date

            termfee_amount = TermFee.objects.filter(meeting__date__gte=latest_cashbox_date).aggregate(Sum('amount'))['amount__sum']
            uniform_amount = Cadet.objects.filter(bond_paid__gte=latest_cashbox_date).count() * 50
            joining_amount = Cadet.objects.filter(joining_fee_paid__gte=latest_cashbox_date).count() * 50
            expense_amount = Expense.objects.filter(meeting__date__gte=latest_cashbox_date).aggregate(Sum('amount'))['amount__sum']
            if termfee_amount is None:
                termfee_amount = 0
            if expense_amount is None:
                expense_amount = 0

            cashbox_amount = cashbox_current + termfee_amount + uniform_amount + joining_amount - expense_amount
            return cashbox_amount
