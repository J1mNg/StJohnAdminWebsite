from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import EditCadetInformationForm

from CadetApp.models import Cadet
from AdminSystem.settings import BASE_DIR

import json
import os

# User defined Helper Functions
def check_admin(user):
   return user.is_superuser

def does_cadet_exist(dems_id):
    try:
        cadet_obj = Cadet.objects.get(dems_id = dems_id)
    except Cadet.DoesNotExist:
        return False

    return True

# Factory Classes
class CadetFactory():
    def createCadet(self, dems_id, first_name, last_name, rank, mobile, email):
        if mobile == "":
            mobile = None

        if not mobile == None:
            mobile = mobile.replace(" ", "")
        
        cadet = Cadet(dems_id = dems_id, firstname = first_name, lastname = last_name, rank = rank, mobile = mobile, email = email, is_active = True)

        return cadet

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

@user_passes_test(check_admin)
def update_cadetDB_view(request):
    template_name = "update_cadetDB_view.html"

    return render(request, template_name)

@user_passes_test(check_admin)
def update_cadetDB(request):
    if request.method == 'GET':
        return redirect('/cadets/update_cadetDB_view/')

    file_path_cadet_list = BASE_DIR + '/CadetApp/cadet_list/cadet_list.json'
    file_path_cadet_hours = BASE_DIR + '/CadetApp/cadet_list/cadet_hours.json'

    try:
        with open(file_path_cadet_list, 'r') as cadet_list_json:
            cadet_list_data = cadet_list_json.read()
        
        with open(file_path_cadet_hours, 'r') as cadet_hours_json:
            cadet_hours_data = cadet_hours_json.read()
    except IOError:
        messages.warning(request, 'Failed to update database. File does not exist. Please contact site admin for help')
        return redirect('/cadets/update_cadetDB_view/')

    cadet_list_obj = json.loads(cadet_list_data)
    cadet_hours_obj = json.loads(cadet_hours_data)

    cadet_factory = CadetFactory()

    # Create Cadet and update information if needed
    for cadet in cadet_list_obj:
        if does_cadet_exist(cadet['user_id']) == False:
            try:
                if cadet['div_name'] == "Bankstown City Cadets":
                    cadet_obj = cadet_factory.createCadet(cadet['user_id'], cadet['first_name'], cadet['last_name'], cadet['rank_abbrev'], cadet['mobile'], cadet['email'])
                    
                    try:
                        cadet_obj.save()
                    except ValueError:
                        messages.warning(request, 'Failed to update database. Please try again and if issue persists, contact admin for support.')
                        break
                else:
                    pass
            except:
                messages.warning(request, 'Unexpected Error. Failed to update database. Please try again and if issue persists, contact admin for support.')
                break
        else:
            cadet_obj = Cadet.objects.get(dems_id = cadet['user_id'])

            try:
                if cadet['mobile'] == "":
                    cadet['mobile'] = None

                if not cadet['mobile'] == None:
                    cadet['mobile'] = cadet['mobile'].replace(" ", "")

                cadet_obj.dems_id = cadet['user_id']
                cadet_obj.firstname = cadet['first_name']
                cadet_obj.lastname = cadet['last_name']
                cadet_obj.rank = cadet['rank_abbrev']
                cadet_obj.mobile = cadet['mobile']
                cadet_obj.email = cadet['email']

                cadet_obj.save()
            except:
                messages.warning(request, 'Failed to update cadet ' + cadet['user_id'])
                pass

    # Update existing cadets with cadet hours
    for cadet in cadet_hours_obj:
        if does_cadet_exist(cadet['id']) == True:
            try:
                cadet_obj = Cadet.objects.get(dems_id = cadet['id'])

                cadet_obj.num_of_events = cadet['count']
                cadet_obj.total_duty_hours = cadet['hours_1']
                cadet_obj.training_hours = cadet['hours_2']
                cadet_obj.other_hours = cadet['hours_3']
                cadet_obj.meeting_hours = cadet['hours_4']

                cadet_obj.save()
            except:
                messages.warning(request, 'Failed to update cadet ' + cadet['id'] + "'s hour information")
                pass
        else:
            pass

    if len(list(messages.get_messages(request))) == 0:
        messages.success(request, 'Cadet Database Successfully Updated')

    return redirect('/cadets/update_cadetDB_view/')