from django.contrib.auth.models import User
from datetime import datetime, timedelta
from fair.tasks.models import Task


def filter_eligible_tasks(task: Task, date: "datetime"):
    queue_items = task.queueitem_set.all()
    for item in queue_items:
        if item.state in ["SCHEDULED", "ACTIVE", "POSTPONED"]:
            return False

    if task.last_completed_at is None:
        return True

    if task.last_completed_at + timedelta(seconds=task.interval) < date:
        return True

    return False


def get_eligible_tasks(*, user: User = None, date: "datetime" = None):
    eligible_tasks = user.taskpool.tasks
    return list(
        filter(lambda task: filter_eligible_tasks(task, date), eligible_tasks.all())
    )
