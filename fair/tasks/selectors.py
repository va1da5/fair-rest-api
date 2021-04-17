from typing import List
from .models import Task
from django.contrib.auth.models import User


def all_task_list() -> List[Task]:
    return Task.objects.all()


def personal_task_list(*, user: User = None) -> List[Task]:
    return user.taskpool.tasks
