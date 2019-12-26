from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from .forms import EditCadetInformationForm

from AdminSystemApp.models import Cadet

# Create your views here.

def home(request):
    return render(request, "home.html")

def cadets(request):
    cadets = Cadet.objects.all()
    
    args = {'cadets': cadets}
    return render(request, "cadets.html", args)

def edit_cadet(request, cadet_id='0'):
    cadet = Cadet.objects.get(user_id=cadet_id)
    
    if request.method == 'POST':
        edit_cadet_form = EditCadetInformationForm(request.POST, instance=cadet)

        if edit_cadet_form.is_valid():
                cadet.firstname = edit_cadet_form.cleaned_data['firstname']
                cadet.lastname = edit_cadet_form.cleaned_data['lastname']

                cadet.save()
        
                return redirect('cadets')
    else:   
        edit_cadet_form = EditCadetInformationForm(instance=cadet)
        args = {'cadet': cadet, 'form': edit_cadet_form}

        return render(request, "editCadet.html", args)

def role_marking(request):
    return render(request, "role_marking.html")

def cash_box(request):
    return render(request, "cash_box.html")
