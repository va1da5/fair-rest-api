from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import QueueItem
from rest_framework.exceptions import NotFound
from rest_framework import generics
from . import selectors, services
from .serializers import QueueItemSerializer, UserSerializer, TaskSerializer


class UserQueueItemsApi(generics.ListAPIView):
    """List of queue items assigned to the current user"""

    serializer_class = QueueItemSerializer

    def get_queryset(self):
        return selectors.personal_queue_item_list(user=self.request.user)


class QueueItemsApi(generics.ListAPIView):
    class OutputSerializer(QueueItemSerializer):
        user = UserSerializer()

        def __init__(self, *args, **kwargs):
            self.Meta.fields.append("user")
            super().__init__(*args, **kwargs)

    serializer_class = OutputSerializer
    queryset = selectors.queue_item_list()


class QueueItemActivateApi(APIView):
    """Activates task queue item"""

    def post(self, request, uuid: str):
        try:
            task_queue_item = selectors.task_queue_item(uuid=uuid)
        except QueueItem.DoesNotExist:
            raise NotFound()
        task_queue_item.activate_task().save()
        data = QueueItemSerializer(task_queue_item).data
        return Response(data)


class QueueItemPostponeApi(APIView):
    """Postpones task queue item"""

    def post(self, request, uuid: str):
        try:
            task_queue_item = selectors.task_queue_item(uuid=uuid)
        except QueueItem.DoesNotExist:
            raise NotFound()
        task_queue_item.postpone_task().save()
        data = QueueItemSerializer(task_queue_item).data
        return Response(data)


class QueueItemCompleteApi(APIView):
    """Postpones task queue item"""

    def post(self, request, uuid: str):
        try:
            task_queue_item = selectors.task_queue_item(uuid=uuid)
        except QueueItem.DoesNotExist:
            raise NotFound()
        task_queue_item.complete_task().save()
        data = QueueItemSerializer(task_queue_item).data
        return Response(data)


class QueueItemRatingApi(APIView):
    """Postpones task queue item"""

    class InputSerializer(serializers.Serializer):
        stars = serializers.IntegerField(max_value=5, min_value=1)

    def post(self, request, uuid: str):
        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            task_queue_item = selectors.task_queue_item(uuid=uuid)
        except QueueItem.DoesNotExist:
            raise NotFound()
        task_queue_item.set_rating(value=serializer.validated_data["stars"]).save()
        data = QueueItemSerializer(task_queue_item).data
        return Response(data)


class EligibleTasksApi(APIView):
    import datetime

    def get(self, request):

        tasks = services.get_eligible_tasks(
            user=self.request.user, date=self.datetime.datetime.now()
        )

        data = TaskSerializer(tasks, many=True).data
        return Response(data)
