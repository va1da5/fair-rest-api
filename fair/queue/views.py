from rest_framework import generics, serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from fair.core.serializers import UserSerializer

from . import selectors
from .models import QueueItem
from .serializers import QueueItemSerializer, QueueItemWithUserSerializer


class UserQueueItemsApi(generics.ListAPIView):
    """List of queue items assigned to the current user"""

    serializer_class = QueueItemSerializer

    def get_queryset(self):
        return selectors.personal_queue_item_list(
            user=self.request.user, household=self.request.household
        )


class QueueItemsApi(generics.ListAPIView):
    serializer_class = QueueItemWithUserSerializer

    def get_queryset(self):
        return selectors.queue_item_list(household=self.request.household)


class QueueItemActivateApi(APIView):
    """Activates task queue item"""

    def post(self, request, uuid: str, **kwargs):
        try:
            task_queue_item = selectors.task_queue_item(uuid=uuid)
        except QueueItem.DoesNotExist:
            raise NotFound()
        task_queue_item.activate_task(request.user).save()
        data = QueueItemSerializer(task_queue_item).data
        return Response(data)


class QueueItemPostponeApi(APIView):
    """Postpones task queue item"""

    def post(self, request, uuid: str, **kwargs):
        try:
            task_queue_item = selectors.task_queue_item(uuid=uuid)
        except QueueItem.DoesNotExist:
            raise NotFound()
        task_queue_item.postpone_task(request.user).save()
        data = QueueItemSerializer(task_queue_item).data
        return Response(data)


class QueueItemCompleteApi(APIView):
    """Postpones task queue item"""

    def post(self, request, uuid: str, **kwargs):
        try:
            task_queue_item = selectors.task_queue_item(uuid=uuid)
        except QueueItem.DoesNotExist:
            raise NotFound()
        task_queue_item.complete_task(request.user).save()
        data = QueueItemSerializer(task_queue_item).data
        return Response(data)


class QueueItemRatingApi(APIView):
    """Postpones task queue item"""

    class InputSerializer(serializers.Serializer):
        stars = serializers.IntegerField(max_value=5, min_value=1)

    def post(self, request, uuid: str, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            task_queue_item = selectors.task_queue_item(uuid=uuid)
        except QueueItem.DoesNotExist:
            raise NotFound()
        task_queue_item.set_stars(
            request.user, value=serializer.validated_data["stars"]
        ).save()
        data = QueueItemSerializer(task_queue_item).data
        return Response(data)
