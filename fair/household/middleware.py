from rest_framework.exceptions import PermissionDenied

from .models import Household


class HouseholdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        household_uuid = view_kwargs.get("household_uuid")
        if not household_uuid:
            return
        try:
            household = Household.objects.filter(
                uuid=household_uuid, members=request.user
            ).get()
            setattr(request, "household", household)
        except Household.DoesNotExist:
            raise PermissionDenied
