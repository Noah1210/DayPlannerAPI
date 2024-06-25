from django.db import models

from DayPlannerAPI import settings


class Note(models.Model):
    content = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
