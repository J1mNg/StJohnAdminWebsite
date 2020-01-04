from django import forms
from functools import partial
import datetime
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

class IndexRedirectForm(forms.Form):
    now = datetime.datetime.now()
    year = forms.IntegerField()
    TERM_CHOICES = [
        (1, 'Term 1'),
        (2, 'Term 2'),
        (3, 'Term 3'),
        (4, 'Term 4'),
    ]
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]
    DAY_CHOICES = [(i,i) for i in range(31)]
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    day = forms.ChoiceField(choices=DAY_CHOICES)
    term  = forms.ChoiceField(choices=TERM_CHOICES)
