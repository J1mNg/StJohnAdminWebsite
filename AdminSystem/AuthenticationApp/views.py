from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import logout
from django.conf import settings

# Create your views here.