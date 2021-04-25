from rest_framework import serializers

from fair.core.serializers import UserSerializer
from fair.tasks.serializers import TaskSerializer

from .models import QueueItem


class QueueItemSerializer(serializers.ModelSerializer):
    task = TaskSerializer()

    class Meta:
        model = QueueItem
        fields = [
            "uuid",
            "state",
            "task",
            "scheduled_at",
            "activated_at",
            "postponed_at",
            "completed_at",
            "stars",
        ]


class QueueItemWithUserSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    user = UserSerializer()

    class Meta:
        model = QueueItem
        fields = [
            "uuid",
            "state",
            "task",
            "user",
            "scheduled_at",
            "activated_at",
            "postponed_at",
            "completed_at",
            "stars",
        ]
