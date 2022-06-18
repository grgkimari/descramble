from django.forms import ModelForm
from .models import Attempt

class AttemptForm(ModelForm):
    class Meta:
        model = Attempt
        fields = ['attemptText']
    