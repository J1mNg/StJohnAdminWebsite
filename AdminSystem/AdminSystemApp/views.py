from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from AdminSystemApp.models import Cadet

# Create your views here.

def home(request):
    return render(request, "home.html")

def cadets(request):
    cadets = Cadet.objects.all()
    
    args = {'cadets': cadets}
    return render(request, "cadets.html", args)

def edit_cadet(request, cadet_id='0'):
    args = {'cadet_id': cadet_id}

    return render(request, "editCadet.html", args)

def role_marking(request):
    return render(request, "role_marking.html")

def cash_box(request):
    return render(request, "cash_box.html")
