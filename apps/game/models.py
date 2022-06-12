from django.db import models
from django.contrib.auth.models import User

class Attempt(models.Model):
    word = models.CharField(max_length=100)
    attemptText = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    isChecked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return self.attemptText + ' ' + str(self.time_created)
