from django.db import models
from DayPlannerAPI import settings
class Task(models.Model):
    title = models.CharField(max_length=50)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    color = models.CharField(max_length=7)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
