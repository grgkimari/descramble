from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
	username = forms.CharField(max_length = 100, widget = forms.TextInput())
	phone_number = forms.CharField(max_length = 25)
	password1 = forms.CharField(max_length = 100, widget = forms.PasswordInput())
	password2 = forms.CharField(max_length = 100, widget = forms.PasswordInput())
	email = forms.EmailField(max_length = 100, widget = forms.TextInput())

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 100, widget = forms.TextInput())
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput())
