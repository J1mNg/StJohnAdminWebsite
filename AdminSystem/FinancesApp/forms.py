from django import forms
from crispy_forms.helper import FormHelper

class IndexRedirectForm(forms.Form):
    year = forms.IntegerField()
    TERM_CHOICES = [
        (1, 'Term 1'),
        (2, 'Term 2'),
        (3, 'Term 3'),
        (4, 'Term 4'),
    ]
    term_finances = forms.ChoiceField(choices=TERM_CHOICES)
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
    month = forms.ChoiceField(choices=MONTH_CHOICES)
    term_termfees = forms.ChoiceField(choices=TERM_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
