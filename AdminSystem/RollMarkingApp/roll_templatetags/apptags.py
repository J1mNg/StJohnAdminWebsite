from django import template
from RollMarkingApp.models import Attendance, Absence

register = template.Library()

@register.filter
def filter_cadet_attendance(cadet, term_date):
    return Attendance.objects.filter(cadet=cadet, meeting=term_date)

@register.filter
def filter_cadet_uniform(cadet, term_date):
    return Attendance.objects.filter(cadet=cadet, meeting=term_date, uniform=True)

@register.filter
def filter_cadet_absence(cadet, term_date):
    return Absence.objects.filter(cadet=cadet, meeting=term_date)

@register.filter
def filter_cadet_absence_reason(cadet, term_date):
    cadet_meeting_obj = Attendance.objects.filter(cadet=cadet, meeting=term_date).values('reason_code')
    return cadet_meeting_obj
