from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from .models import Attempt

class AttemptForm(ModelForm):
    class Meta:
        model = Attempt
        fields = ['attemptText']
    