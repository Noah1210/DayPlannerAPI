from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=50)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    color = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
