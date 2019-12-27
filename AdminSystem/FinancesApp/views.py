from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
def index(request):
    return render(request, "finances_index.html")