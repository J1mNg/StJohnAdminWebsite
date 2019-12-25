from django.shortcuts import render

# Create your views here.

def databases_index(request):
    return render(request, "DatabasesApp/viewDatabases_base.html")
