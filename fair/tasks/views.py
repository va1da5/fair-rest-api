from rest_framework import generics

from . import selectors
from .serializers import TaskSerializer


class TaskListApi(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return selectors.household_task_list(household=self.request.household)


class PersonalTasksApi(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return selectors.personal_task_list(
            user=self.request.user, household=self.request.household
        )
