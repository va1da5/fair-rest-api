from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.HouseholdListApi.as_view(), name="list"),
    path("<str:household_uuid>", views.HousehostRetrieveApi.as_view(), name="list"),
]
