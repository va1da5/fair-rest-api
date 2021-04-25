from typing import List

from django.contrib.auth.models import User

from fair.household.models import Household

from .models import QueueItem


def personal_queue_item_list(*, user: User, household: Household) -> List[QueueItem]:
    return QueueItem.objects.filter(user=user, task__household=household).all()


def queue_item_list(*, household: Household) -> List[QueueItem]:
    return QueueItem.objects.filter(task__household=household).all()


def task_queue_item(*, uuid: str = None) -> QueueItem:
    return QueueItem.objects.get(uuid=uuid)
