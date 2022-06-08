from django.shortcuts import render
from .forms import AttemptForm

def homePage(request):
    return render(request,'game/homepage.html')
