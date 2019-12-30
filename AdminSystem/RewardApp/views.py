from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from .forms import EditCadetInformationForm

# from RewardApp.models import Reward

# Create your views here.
def reward_index(request):
    return render(request, "reward_index.html")