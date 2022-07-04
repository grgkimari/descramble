from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import CustomUser 

class SignupForm(UserCreationForm):
	model = CustomUser
	fields = ['email', 'password1', 'password2']

class LoginForm(forms.Form):
	email = forms.EmailField(max_length = 100)
	password = forms.CharField(max_length = 100)