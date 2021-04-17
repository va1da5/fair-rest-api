from .models import QueueItem
from rest_framework import serializers
from fair.tasks.serializers import TaskSerializer
from fair.core.serializers import UserSerializer


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
        ]
