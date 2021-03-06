from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

from fair.household.models import Household


class Task(models.Model):
    uuid = models.UUIDField(verbose_name="Task ID", unique=True, default=uuid4)
    name = models.CharField(max_length=100, verbose_name="Name", help_text="Task name")
    description = models.TextField(verbose_name="Description")
    interval = models.IntegerField(
        verbose_name="Interval", help_text="Interval in seconds"
    )
    time_to_complete = models.IntegerField(
        verbose_name="Takes Time",
        help_text="How much time on average does it take to complete the task in seconds",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    last_completed_at = models.DateTimeField(default=None, null=True, blank=True)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    handlers = models.ManyToManyField(User, help_text="Task handlers")

    def __repr__(self) -> str:
        return f"<Task: {self.name} - {self.household.name}>"

    def __str__(self) -> str:
        return self.__repr__()
