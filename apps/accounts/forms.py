from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import CustomUser 

class SignupForm(UserCreationForm):
	model = CustomUser
	fields = ['email', 'password1', 'password2']

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 100, widget = forms.TextInput())
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput())