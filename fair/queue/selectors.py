from typing import List
from django.contrib.auth.models import User
from .models import QueueItem


def personal_queue_item_list(*, user: User = None) -> List[QueueItem]:
    return QueueItem.objects.filter(user=user).all()


def queue_item_list() -> List[QueueItem]:
    return QueueItem.objects.all()


def task_queue_item(*, uuid: str = None) -> QueueItem:
    return QueueItem.objects.get(uuid=uuid)
