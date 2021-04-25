from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class HouseholdUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_scheduled_tasks = models.IntegerField(
        verbose_name="Max Scheduled Tasks",
        help_text="Maximum number of allowed scheduled tasks",
        default=1,
        validators=[
            MinValueValidator(1, message="Rating is to small"),
            MaxValueValidator(5, message="Rating to too large"),
        ],
    )

    def __repr__(self) -> str:
        return f"<HouseholdUser: {self.user.username}>"

    def __str__(self) -> str:
        return self.__repr__()


class Household(models.Model):
    uuid = models.UUIDField(verbose_name="Household ID", unique=True, default=uuid4)
    name = models.CharField(
        max_length=100, verbose_name="Name", help_text="Household name"
    )
    members = models.ManyToManyField(User, help_text="Household member list")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f"<Household: {self.name}>"

    def __str__(self) -> str:
        return self.__repr__()
