from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, CreateView, DeleteView
from django.core.exceptions import ValidationError
from .models import Meeting, Cadet, Attendance, Absence
from .forms import MeetingForm_AddAll, IndexRedirectForm
from dateutil import rrule
from datetime import datetime, timedelta

from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

def rollmarkingIndex(request):
    now = datetime.now()
    if request.method == 'POST': #& IndexRedirectForm.base_fields.keys():
        get_request = request.POST
        form = IndexRedirectForm(get_request)
        if form.is_valid():
            data = form.cleaned_data
            if 'go_mark_attendance' in get_request:
                return redirect('rollmarking:mark_attendance', year=data['year'], month=data['month'], day=data['day'])
            elif 'go_view_attendance' in get_request:
                return redirect('rollmarking:view_attendance', year=data['year'], term=data['term'])

    else:
        #initial doesn't work
        form = IndexRedirectForm(initial={'year':now.year, 'month':now.month, 'day':now.day})

    return render(request, 'RollMarkingApp/rollmark_index.html', {'form': form})

#add validation for end_date > start_date
#prevent users from selecting term if it exists already
#redirect to appropriate page
def form_addmeetings(request):
    if request.method == 'POST':
        form = MeetingForm_AddAll(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            term = data['term']
            start_date = data['start_date']
            end_date = data['end_date']
            for dt in rrule.rrule(rrule.WEEKLY, dtstart = start_date, until = end_date):
                meeting_data = Meeting(term=term, date=dt.strftime("%Y-%m-%d"))
                meeting_data.save()
    else:
        form = MeetingForm_AddAll()

    return render(request, 'RollMarkingApp/meeting_form.html', {'form': form})

def mark_attendance(request, year, month, day):
    cadets = Cadet.objects.filter(is_active=True)
    context = {'cadets':cadets}

    if request.method == 'POST':
        meeting = Meeting.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day)
        for cadet in request.POST.getlist('cadet_attendance'):
            if meeting.exists():
                attendance = Attendance(cadet=Cadet.objects.get(pk=cadet), meeting=meeting[0], uniform=False)
                Attendance.clean(attendance)
                attendance.save()
            else:
                context = {'cadets':cadets, 'messages':'Meeting does not exist'}
                return render(request, 'RollMarkingApp/mark_attendance.html', context)

        for uniform in request.POST.getlist('cadet_uniform'):
            cadet = Cadet.objects.get(pk=uniform)
            cadet.uniform = True
            cadet.save()

        #fix, write javascript -> if cadet attended checkbox is ticked, then don't submit absence
        for cadet in request.POST.getlist('cadet_absence'):
            exit = True
            for check in request.POST.getlist('cadet_attendance'):
                if check == cadet[1]:
                    exit = False

            if exit:
                if meeting.exists():
                    absence = Absence(cadet=Cadet.objects.get(pk=int(cadet[1])), meeting=meeting[0], reason_code=cadet[0])
                    Absence.clean(absence)
                    absence.save()
                else:
                    context = {'cadets':cadets, 'messages':'Meeting does not exist'}
                    return render(request, 'RollMarkingApp/mark_attendance.html', context)


    return render(request, 'RollMarkingApp/mark_attendance.html', context)

class AttendanceCreateView(SuccessMessageMixin, CreateView):
    model = Attendance
    template_name = 'RollMarkingApp/cadet_attendance_form.html'
    fields = '__all__'
    success_url = reverse_lazy('rollmarking:rollMarkingIndex')
    success_message = "%(cadet)s attendance successfully entered"

# reason codes don't work yet
def view_attendance(request, year, term):
    attendance = Attendance.objects.all()
    cadets = Cadet.objects.filter(is_active=True)
    term_dates = Meeting.objects.filter(term=term).filter(date__year=year)

    context = {'cadets':cadets, 'term_dates':term_dates, 'attendance':attendance}
    return render(request, 'RollMarkingApp/view_attendance.html', context)
