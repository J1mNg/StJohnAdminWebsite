from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class MeetingForm_AddAll(forms.Form):
    TERM_CHOICES = [
        (1, 'Term 1'),
        (2, 'Term 2'),
        (3, 'Term 3'),
        (4, 'Term 4'),
    ]
    term = forms.ChoiceField(
        choices=TERM_CHOICES,
        initial='',
        widget=forms.Select(),
        required=True
    )
    start_date = forms.DateField(widget=DateInput(), required=True)
    end_date = forms.DateField(widget=DateInput(), required=True)

# class AttendanceForm(forms.Form):
#     cadet_attendance = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple(), required = False)
#     #cadet_uniform = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple())
#     #cadet_absence = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple())


# class MeetingForm_Add_Delete(forms.Form):
#     TERM_CHOICES = [
#         (1, 'Term 1'),
#         (2, 'Term 2'),
#         (3, 'Term 3'),
#         (4, 'Term 4'),
#     ]
#     term = forms.ChoiceField(
#         choices=TERM_CHOICES,
#         initial='',
#         widget=forms.Select(),
#         required=True
#     )
#     date_to_delete = forms.DateField(widget=DateInput(), required=True)
