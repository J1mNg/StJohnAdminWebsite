from django import template
from FinancesApp.models import TermFee, Expense
from CadetApp.models import Cadet

register = template.Library()

def return_termfee_total(date):
    amount_list = TermFee.objects.filter(meeting__date=date).values_list('amount',flat=True)
    termfee_total = 0
    for amount in amount_list:
        termfee_total += amount

    return termfee_total

def return_uniformbond_total(date):
    amount_list = Cadet.objects.filter(bond_paid=date)
    uniformbond_total = 0
    for item in amount_list:
        uniformbond_total += 50

    return uniformbond_total

def return_joiningfee_total(date):
    amount_list = Cadet.objects.filter(joining_fee_paid=date)
    joiningfee_total = 0
    for item in amount_list:
        joiningfee_total += 50

    return joiningfee_total


def return_expense_total(date):
    amount_list = Expense.objects.filter(meeting__date=date).values_list('amount',flat=True)
    expense_total = 0
    for amount in amount_list:
        expense_total += amount

    return expense_total

@register.filter
def filter_termfees(date):
    return return_termfee_total(date)

@register.filter
def filter_uniformbond(date):
    return return_uniformbond_total(date)

@register.filter
def filter_joiningfee(date):
    return return_joiningfee_total(date)

@register.filter
def filter_income(date):
    return return_termfee_total(date) + return_uniformbond_total(date) + return_joiningfee_total(date)

@register.filter
def filter_expenses(date):
    return return_expense_total(date)

@register.filter
def filter_profit(date):
    return return_termfee_total(date) + return_uniformbond_total(date) + return_joiningfee_total(date) - return_expense_total(date)
