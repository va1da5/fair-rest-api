from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "uuid",
            "name",
            "description",
            "interval",
            "time_to_complete",
            "last_completed_at",
        )
