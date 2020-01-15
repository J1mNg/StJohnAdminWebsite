from django.contrib import admin
from .models import TermFee, Expense, CashBox

# Register your models here.

admin.site.register(TermFee)
admin.site.register(Expense)
admin.site.register(CashBox)
