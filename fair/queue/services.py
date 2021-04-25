import itertools
from datetime import datetime, timedelta
from typing import List

from django.contrib.auth.models import User

from fair.household.models import Household
from fair.tasks.models import Task

from .exceptions import HandlerNotAvailable, ValidHandlerUnavailable
from .models import QueueItem


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


def is_handler_available(user: User) -> bool:
    number_of_scheduled_tasks = user.queueitem_set.filter(state="SCHEDULED").count()
    if user.householduser.max_scheduled_tasks > number_of_scheduled_tasks:
        print()
        return True
    raise ValidHandlerUnavailable(
        f"User @{user.username} has limit of {user.householduser.max_scheduled_tasks} "
        "scheduled tasks and cannot accept any additional tasks at this moment"
    )


def get_handler(*, task: Task) -> User:
    handler_count = task.handlers.count()
    if handler_count == 0:
        raise HandlerNotAvailable("The task '{task.name}' is missing assigned handlers")

    handlers = task.handlers.all()

    if handler_count == 1:
        is_handler_available(handlers[0])
        return handlers[0]

    completed_count = task.queueitem_set.count()
    if completed_count == 0:
        for user in handlers:
            try:
                is_handler_available(user)
                return user
            except ValidHandlerUnavailable as exc:
                print(exc)
                continue
        else:
            raise HandlerNotAvailable(
                f"No valid handlers where found for task '{task.name}' at this time"
            )

    last_completed = task.queueitem_set.latest("completed_at")

    handlers_circle = itertools.cycle(handlers)

    for _ in range(handler_count):
        user = next(handlers_circle)
        if user == last_completed.user:
            next_hander = next(handlers_circle)
            is_handler_available(next_hander)
            return next_hander

    raise HandlerNotAvailable(f"No valid handlers where found for task '{task.name}'")


def get_outstanding_tasks(*, household: Household, date: "datetime") -> List[Task]:
    household_tasks = household.task_set.all()
    return list(
        filter(
            lambda task: filter_eligible_tasks(task, date),
            household_tasks,
        )
    )


def schedule_task(*, task: Task, handler: User):
    queue_item = QueueItem(user=handler, task=task)
    queue_item.save()


def schedule_tasks(*, date: "datetime"):
    households = Household.objects.all()

    for household in households:
        outstanding_tasks = get_outstanding_tasks(household=household, date=date)

        for task in outstanding_tasks:
            try:
                handler = get_handler(task=task)
                schedule_task(task=task, handler=handler)
            except (HandlerNotAvailable, ValidHandlerUnavailable) as exc:
                print(exc)

    return outstanding_tasks
