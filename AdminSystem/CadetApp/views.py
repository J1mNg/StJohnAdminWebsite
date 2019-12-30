from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import EditCadetInformationForm

from CadetApp.models import Cadet

# Create your views here.
def index(request):
    return render(request, "cadets_index.html")

@login_required
def cadets(request):
    cadets = Cadet.objects.all()
    query = request.GET.get('q')
    if query:
        query_list = cadets.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query) |
            Q(email__icontains=query) |
            Q(rank__icontains=query) |
            Q(qualification__icontains=query)
        ).distinct()

        if not query_list:
            messages.info(request, "Cadet not found. Try Again with different keywords.")
            args = {'cadets': cadets}
            return render(request, "cadets.html", args)
        else:
            args = {'cadets': query_list}
            return render(request, "cadets.html", args)

    args = {'cadets': cadets}
    return render(request, "cadets.html", args)

@login_required
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

@login_required
def add_cadet(request):
    form = EditCadetInformationForm(request.POST or None)
    if form.is_valid():
        form.save()
        cadets = Cadet.objects.all()
        args = {'cadets': cadets}

        return redirect('/cadets/', args)

    args = {
        'form':form
    }

    return render(request, "add_cadet.html", args)