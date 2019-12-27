from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponse

def homepage(request):
    return render(request, "index.html")