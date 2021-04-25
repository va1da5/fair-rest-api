from typing import List

from django.contrib.auth.models import User

from fair.household.models import Household

from .models import Task


def household_task_list(*, household: Household) -> List[Task]:
    return Task.objects.filter(household=household).all()


def personal_task_list(*, user: User, household: Household) -> List[Task]:
    return user.task_set.filter(household=household).all()
