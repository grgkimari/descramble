from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    password1 = models.CharField(max_length = 100)
    password2 = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    currentScore = models.DecimalField(decimal_places=0, max_digits=6, default=0)
    highscores = models.CharField(max_length=100)