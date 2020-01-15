from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, CreateView, DeleteView
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Meeting, Cadet, Attendance, Absence
from .forms import MeetingForm_AddAll, IndexRedirectForm
from dateutil import rrule
from datetime import datetime, timedelta

from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

@login_required
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
            elif 'go_add_meetings' in get_request:
                return redirect('rollmarking:form_addmeetings')


    else:
        #initial doesn't work
        form = IndexRedirectForm(initial={'year':now.year, 'month':now.month, 'day':now.day})

    return render(request, 'RollMarkingApp/rollmark_index.html', {'form': form})

#add validation for end_date > start_date
#prevent users from selecting term if it exists already
#redirect to appropriate page
@login_required
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

@login_required
def mark_attendance(request, year, month, day):
    cadets = Cadet.objects.filter(is_active=True)
    context = {'cadets':cadets}
    #filter for the meeting object with date passed into URL (only 1)
    meeting = Meeting.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day)

    #if there is no object from filter, then meeting does not exist
    if not meeting.exists():
        messages.add_message(request, messages.INFO, 'Meeting does not exist.')
        return render(request, 'RollMarkingApp/mark_attendance.html', context)

    def enter_attendance_into_database():
        # this is here in case button is clicked
        if not meeting.exists():
            messages.add_message(request, messages.INFO, 'Meeting does not exist.')
            return render(request, 'RollMarkingApp/mark_attendance.html', context)

        # checkboxes named 'cadet_attendance' and 'cadet_uniform'
        # if checkboxes are selected then getlist returns [1,2,7,10 ...]
        # which are the primary keys of cadets who attended/wore uniform

        # dropbown menu named 'cadet_absence'
        # getlist returns ['u1', 'u2', 'u3', 'r4'...]
        # which are reason codes and primary keys of cadets who are absent
        # contains primary key of all cadets, even if they are present
        attendances = request.POST.getlist('cadet_attendance')
        uniforms = request.POST.getlist('cadet_uniform')
        absences = request.POST.getlist('cadet_absence')

        # if they are in getlist of attendance, record attendance in database
        for cadet in attendances:
            if cadet in uniforms:
                attendance = Attendance(cadet=Cadet.objects.get(pk=cadet), meeting=meeting[0], uniform=True)
            else:
                attendance = Attendance(cadet=Cadet.objects.get(pk=cadet), meeting=meeting[0], uniform=False)
            #clean method to make sure if a cadet is in attendance table, then can't be in absent table on same date
            attendance.clean()
            attendance.save()

        # if they are in getlist of absences, record absence in database
        for cadet in absences:
            # cadets are absent if in absences but no in attendances
            # 'u3' --> cadet[1] gives primary key --> cadet[0] gives reason code
            if not cadet[1] in attendances:
                absence = Absence(cadet=Cadet.objects.get(pk=int(cadet[1])), meeting=meeting[0], reason_code=cadet[0])
                absence.clean()
                absence.save()

    cadet_attendance = Attendance.objects.filter(meeting__date__year=year).filter(meeting__date__month=month).filter(meeting__date__day=day)
    cadet_absence = Absence.objects.filter(meeting__date__year=year).filter(meeting__date__month=month).filter(meeting__date__day=day)
    # if entry for attendance has been made on a particular date --> update table
    if cadet_attendance.exists() and cadet_absence.exists():
        if request.method == 'POST':
            # delete old attendance data and submit new data
            cadet_attendance.delete()
            cadet_absence.delete()
            enter_attendance_into_database()
            messages.add_message(request, messages.INFO, 'Successfully updated roll')
        else:
            cadet_attendance_dict = cadet_attendance.values('cadet')
            cadet_absence_dict = cadet_absence.values('cadet')
            # may have new cadets in database since roll was marked in past
            # get queryset of cadets in the past --> combine them using union
            cadets = cadets.filter(user_id__in=cadet_attendance_dict.union(cadet_absence_dict))

            # create list of True and False --> if they attended/wore uniform/ were absence_list
            # send as context data for rendering in template --> gets original state of checkboxes
            # [True, False, True ...] --> attendances --> first cadet attended, second didn't, third attended ...
            attendance_list = []
            uniform_list=[]
            absence_list=[]

            for cadet in cadets:
                if cadet_attendance.filter(cadet=cadet).exists():
                    attendance_list.append(True)
                    absence_list.append(False)
                    if cadet_attendance.filter(cadet=cadet, uniform=True).exists():
                        uniform_list.append(True)
                    else:
                        uniform_list.append(False)
                else:
                    attendance_list.append(False)
                    uniform_list.append(False)
                    absence_list.append(cadet_absence.filter(cadet=cadet).values_list('reason_code', flat=True)[0])

            # zip together, so can iterate together
            context = {'zip':zip(cadets, attendance_list, uniform_list, absence_list)}



    elif request.method == 'POST':
        enter_attendance_into_database()
        messages.add_message(request, messages.INFO, 'Successfully marked roll')

    return render(request, 'RollMarkingApp/mark_attendance.html', context)

class AttendanceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Attendance
    template_name = 'RollMarkingApp/cadet_attendance_form.html'
    fields = '__all__'
    success_url = reverse_lazy('rollmarking:rollMarkingIndex')
    success_message = "%(cadet)s attendance successfully entered"

# reason codes don't work yet
@login_required
def view_attendance(request, year, term):
    attendance = Attendance.objects.all()
    cadets = Cadet.objects.filter(is_active=True)
    term_dates = Meeting.objects.filter(term=term).filter(date__year=year)

    context = {'cadets':cadets, 'term_dates':term_dates, 'attendance':attendance}
    return render(request, 'RollMarkingApp/view_attendance.html', context)
