from django.db import models
from django.contrib.auth.models import User

from apps.accounts.models import CustomUser

class Attempt(models.Model):
    word = models.CharField(max_length=100)
    attemptText = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return str(self.id)+ ' ' + self.word + ' ' + str(self.time_created)

class HighScore(models.Model):
    timeSet = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(verbose_name="HighScore", null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ['score']
    
    def __str__(self) -> str:
        return self.user.email + ' : ' + str(self.score) + ' : ' + str(self.timeSet)