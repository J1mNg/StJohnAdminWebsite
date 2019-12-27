from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from .forms import EditCadetInformationForm

from CadetApp.models import Cadet

# Create your views here.
def index(request):
    return render(request, "cadets_index.html")

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
        
                cadets = Cadet.objects.all()
    
                args = {'cadets': cadets}
                return render(request, "cadets.html", args)
    else:   
        edit_cadet_form = EditCadetInformationForm(instance=cadet)
        args = {'cadet': cadet, 'form': edit_cadet_form}

        return render(request, "editCadet.html", args)