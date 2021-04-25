from functools import wraps
from typing import Callable
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from fair.tasks.models import Task


def validate_owner(func) -> Callable:
    @wraps(func)
    def validate(self, user: User, *args, **kwargs):
        if not user == self.user:
            return self
        return func(self, *args, **kwargs)

    return validate


def from_state(allowed_states):
    def inner(func):
        @wraps(func)
        def wrapper(self):
            if self.state not in allowed_states:
                return self
            return func(self)

        return wrapper

    return inner


class QueueItem(models.Model):
    TASK_STATES = [
        ("SCHEDULED", "Scheduled"),
        ("ACTIVE", "Active"),
        ("POSTPONED", "Postponed"),
        ("COMPLETED", "Completed"),
    ]

    uuid = models.UUIDField(verbose_name="Task Queue ID", unique=True, default=uuid4)
    state = models.CharField(
        max_length=15,
        choices=TASK_STATES,
        default="SCHEDULED",
        verbose_name="Task status",
        help_text="Current task state",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Assigned user")
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, help_text="Task to be done"
    )
    postpone_counter = models.IntegerField(
        verbose_name="Postpone Count",
        help_text="How many time the task was postponed",
        default=0,
    )
    stars = models.IntegerField(
        verbose_name="Self rate",
        help_text="Self evaluation for the completion of the task in range of 1-5 starts",
        default=None,
        validators=[
            MinValueValidator(1, message="Rating is to small"),
            MaxValueValidator(5, message="Rating to too large"),
        ],
        blank=True,
        null=True,
    )
    scheduled_at = models.DateTimeField(
        help_text="Time when the task was scheduled", auto_now_add=True
    )
    activated_at = models.DateTimeField(
        help_text="Time when started working on the task",
        default=None,
        null=True,
        blank=True,
    )
    postponed_at = models.DateTimeField(
        help_text="Time when task was postponed",
        default=None,
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        help_text="Time when task was completed",
        default=None,
        null=True,
        blank=True,
    )

    @from_state(["POSTPONED"])
    def reschedule_task(self):
        self.state = "SCHEDULED"
        return self

    @validate_owner
    @from_state(["SCHEDULED", "POSTPONED"])
    def activate_task(self):
        self.state = "ACTIVE"
        self.activated_at = timezone.now()
        return self

    @validate_owner
    @from_state(["SCHEDULED", "POSTPONED"])
    def postpone_task(self):
        self.state = "POSTPONED"
        self.postpone_counter += 1
        self.postponed_at = timezone.now()
        self.activated_at = None
        return self

    @validate_owner
    @from_state(["ACTIVE"])
    def complete_task(self):
        self.state = "COMPLETED"
        self.completed_at = timezone.now()
        self.task.last_completed_at = self.completed_at
        self.task.save()
        return self

    @validate_owner
    @from_state(["COMPLETED"])
    def set_stars(self, value: int):
        if not self.stars:
            self.stars = value
        return self

    def __repr__(self) -> str:
        return f"<QueueItem: {self.user.username} - {self.task.name}>"

    def __str__(self) -> str:
        return self.__repr__()
