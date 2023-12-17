from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    is_done = models.BooleanField()
    is_priority = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)