from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, "home.html")

def cadets(request):
    return render(request, "cadets.html")

def role_marking(request):
    return render(request, "role_marking.html")

def cash_box(request):
    return render(request, "cash_box.html")

