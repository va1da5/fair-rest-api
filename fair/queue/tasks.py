from django.utils import timezone

from celery import shared_task

from .services import schedule_tasks


@shared_task
def schedule_outstanding_tasks():
    schedule_tasks(date=timezone.now())
