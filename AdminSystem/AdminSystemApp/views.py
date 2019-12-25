from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from AdminSystemApp.models import Cadet

# Create your views here.

def home(request):
    return render(request, "home.html")

def cadets(request):
    cadets = Cadet.objects.all()

    args = { 'name': name }
    return render(request, "cadets.html", args)


def role_marking(request):
    return render(request, "role_marking.html")

def cash_box(request):
    return render(request, "cash_box.html")