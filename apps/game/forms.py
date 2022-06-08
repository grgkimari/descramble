from django import forms

class AttemptForm(forms.Form):
    attemptText = forms.CharField(max_length = 100, widget = forms.TextInput())