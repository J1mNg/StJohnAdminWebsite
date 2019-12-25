from django.shortcuts import render

# Create your views here.

def finances_index(request):
    return render(request, "FinancesApp/finances_base.html")
