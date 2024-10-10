from django import forms
from django.core.validators import MinLengthValidator,MaxLengthValidator,ProhibitNullCharactersValidator,RegexValidator,EmailValidator

class ScrapingForm(forms.Form):
    quey_parameter = forms.CharField(
        max_length=100, 
        help_text='filter_option',
        required=True,
        strip=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Search for anything you like...'
        }),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200),
            RegexValidator(regex='^[a-zA-Z- ]+$',message='This field contain invalid characters.')
        ]
    )
    
