from django import forms
from homepage.models import CustomUser, Ticket


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateTicket(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.CharField(widget=forms.Textarea)

