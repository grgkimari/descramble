from csv import field_size_limit
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.accounts.models import User

class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'email']
	# username = forms.CharField(max_length = 100, widget = forms.TextInput())
	# phone_number = forms.CharField(max_length = 25)
	# password1 = forms.CharField(max_length = 100, widget = forms.PasswordInput())
	# password2 = forms.CharField(max_length = 100, widget = forms.PasswordInput())
	# email = forms.EmailField(max_length = 100, widget = forms.TextInput())

class EditUserForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'email']

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 100, widget = forms.TextInput())
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput())