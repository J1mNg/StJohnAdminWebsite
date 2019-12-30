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