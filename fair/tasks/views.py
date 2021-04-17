from rest_framework import generics
from . import selectors
from .serializers import TaskSerializer


class TaskListApi(generics.ListAPIView):
    queryset = selectors.all_task_list()
    serializer_class = TaskSerializer


class PersonalTaskPoolApi(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return selectors.personal_task_list(user=self.request.user)
