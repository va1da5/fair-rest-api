from django.urls import path, include
from . import views


task_patterns = [
    path("", views.TaskListApi.as_view(), name="all"),
    path("my", views.PersonalTaskPoolApi.as_view(), name="personal"),
]


urlpatterns = [
    path("tasks/", include((task_patterns, "tasks"))),
]
