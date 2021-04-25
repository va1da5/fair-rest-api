from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

from .models import Household


class CanAccessHousehold(BasePermission):
    def has_permission(self, request, view):
        household_uuid = view.kwargs.get("household_uuid")
        count = Household.objects.filter(
            uuid=household_uuid, members=request.user
        ).count()
        if count == 1:
            return True
        return False
