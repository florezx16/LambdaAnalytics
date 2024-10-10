from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

#Create here your forms
class CustomUserMainForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','phone_number','gender','is_staff','password']
        labels = {
            'is_staff':'Admin role'
        }
        help_texts = {
            'is_staff':'Indicates if the main role is Admin or normal'
        }
        widgets = {
            'username':forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'first_name':forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'last_name':forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'phone_number':forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'gender':forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),
            'is_staff':forms.CheckboxInput(
                attrs={
                    'class':'form-check-input'
                }
            ),
            'password':forms.PasswordInput(
                attrs={
                    'class':'form-control'
                }
            )
        }

class CustomUserLoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    
    def clean_username(self):#Check username exist
        username2check = self.cleaned_data.get('username')
        if not CustomUser.objects.filter(username=username2check).exists():
            raise ValidationError("This username doesn't exist.")
        return username2check

class CustomUserPasswordUpdateForm(forms.Form):
    password = forms.CharField(
        label='New password',help_text='Secret key',
        widget=forms.PasswordInput(
            attrs={'class':'form-control'}
        )
    )
    
    password_repeat = forms.CharField(
        label='Repeat password',help_text='Secret key(again)',
        widget=forms.PasswordInput(
            attrs={'class':'form-control'}
        )
    )
    
    def clean_password_repeat(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if (password and password_repeat) and (password != password_repeat):
            raise ValidationError("Password fields must match.")
        return password_repeat
