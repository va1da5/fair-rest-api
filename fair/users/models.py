from django.contrib.auth.models import User
from django.db import models
from fair.tasks.models import Task


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task)
