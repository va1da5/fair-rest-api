from django.urls import include, path

from . import views

task_patterns = [
    path("", views.TaskListApi.as_view(), name="all"),
    path("my", views.PersonalTasksApi.as_view(), name="personal"),
]


urlpatterns = [
    path("tasks/", include((task_patterns, "tasks"))),
]
