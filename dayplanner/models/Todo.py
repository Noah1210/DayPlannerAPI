from django.db import models
from DayPlannerAPI import settings


class Todo(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    is_done = models.BooleanField()
    is_priority = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)