from django import forms
from django.forms import TextInput, NumberInput, EmailInput, DateInput, CheckboxInput, ModelForm
from .models import Cadet

import datetime

class EditCadetInformationForm(ModelForm):
    class Meta:
        model = Cadet

        fields = [
            'firstname',
            'lastname',
            'birthday',
            'age',
            'mobile',
            'email',
            'date_joined',
            'years_since_joined',
            'bond_paid',
            'joining_fee_paid',
            'rank',
            'qualification',
            'total_duty_hours',
            'num_of_events',
            'training_hours',
            'other_hours',
            'meeting_hours',
            'is_active',
        ]

        widgets = {
            'firstname': TextInput(
                attrs={
                    'class': 'form_input',
                    'placeholder': 'firstname'
                }
            ),
            'lastname': TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'lastname'
            }),
            'birthday': DateInput(attrs={
                'class': 'form_input',
                'placeholder': 'birthday',
                'type': 'date',
            }),
            'age': NumberInput(attrs={
                'class': 'form_input',
                'placeholder': 'age'
            }),
            'mobile': NumberInput(attrs={
                'class': 'form_input',
                'placeholder': 'mobile number'
            }),
            'email': EmailInput(attrs={
                'class': 'form_input',
                'placeholder': 'email address'
            }),
            'date_joined': DateInput(attrs={
                'class': 'form_input',
                'placeholder': 'birthday',
                'type': 'date',
            }),
            'years_since_joined':NumberInput(attrs={
                'class': 'form_input',
                'placeholder': 'age'
            }),
            'bond_paid': DateInput(attrs={
                'class': 'form_input',
                'placeholder': 'number of years since joining',
                'type': 'date',
            }),
            'joining_fee_paid': DateInput(attrs={
                'class': 'form_input',
                'placeholder': 'date of joining fee payment',
                'type': 'date',
            }),
            'rank': TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'rank'
            }),
            'qualification': TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'qualifications'
            }),
            'total_duty_hours':NumberInput(attrs={
                'class': 'form_input',
                'placeholder': 'total number of duty hours'
            }),
            'num_of_events':NumberInput(attrs={
                'class': 'form_input',
                'placeholder': 'total number of events attended'
            }),
            'training_hours':NumberInput(attrs={
                'class': 'form_input',
                'placeholder': 'total training hours completed'
            }),
            'other_hours':NumberInput(attrs={
                'class': 'form_input',
                'placeholder': 'total other hours committed'
            }),
            'meeting_hours':NumberInput(attrs={
                'class': 'form_input',
                'placeholder': 'total meeting hours attended'
            }),
            'is_active':CheckboxInput(attrs={
                'class': 'form_input',
            }),
        }
