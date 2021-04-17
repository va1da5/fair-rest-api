from django.urls import path, include
from . import views

queue_patterns = [
    path("", views.QueueItemsApi.as_view(), name="list"),
    path("my", views.UserQueueItemsApi.as_view(), name="my"),
    path(
        "<str:uuid>/activate",
        views.QueueItemActivateApi.as_view(),
        name="item.activate",
    ),
    path(
        "<str:uuid>/postpone",
        views.QueueItemPostponeApi.as_view(),
        name="item.postpone",
    ),
    path(
        "<str:uuid>/complete",
        views.QueueItemCompleteApi.as_view(),
        name="item.complete",
    ),
    path(
        "<str:uuid>/evaluate",
        views.QueueItemRatingApi.as_view(),
        name="item.rank",
    ),
    path("eligible", views.EligibleTasksApi.as_view(), name="eligible"),
]

urlpatterns = [
    path("queue/", include((queue_patterns, "queue"))),
]
