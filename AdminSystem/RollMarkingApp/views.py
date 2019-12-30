from django.shortcuts import render
#from django.view.generic import CreateView
from .models import Meeting, Cadet, Attendance, Absence
from .forms import MeetingForm_AddAll
from dateutil import rrule
from datetime import datetime, timedelta

# Create your views here.

# Create your views here.
def index(request):
    return render(request, "rollmark_index.html")

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

    return render(request, 'meeting_form.html', {'form': form})

def mark_attendance(request, year, month, day):
    cadets = Cadet.objects.filter(is_active=True)

    if request.method == 'POST':
        for cadet in request.POST.getlist('cadet_attendance'):
            attendance = Attendance(cadet=Cadet.objects.get(pk=cadet), meeting=Meeting.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day)[0], uniform=False)
            attendance.save()

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
                absence = Absence(cadet=Cadet.objects.get(pk=int(cadet[1])), meeting=Meeting.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day)[0], reason_code=cadet[0])
                absence.save()

    context = {'cadets':cadets}
    return render(request, 'mark_attendance.html', context)

# reason codes don't work yet
def view_attendance(request, year, term):
    attendance = Attendance.objects.all()
    cadets = Cadet.objects.filter(is_active=True)
    term_dates = Meeting.objects.filter(term=term).filter(date__year=year)

    context = {'cadets':cadets, 'term_dates':term_dates, 'attendance':attendance}
    return render(request, 'view_attendance.html', context)


# be able to delete or add individual meetings

# def form_deletemeetings(request):
#     if request.method == 'POST':
#         form = MeetingForm_Add_Delete(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#
#             term = data['term']
#
#     else:
#         form = MeetingForm_Add_Delete()
#
#     return render(request, 'RollMarkingApp/meeting_form.html', {'form': form})
