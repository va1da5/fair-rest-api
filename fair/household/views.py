from rest_framework import generics
from rest_framework.response import Response

from . import permissions
from .models import Household
from .serializers import HouseholdWithMembersSerializer, MinimalHouseholdSerializer


class HouseholdListApi(generics.ListAPIView):
    queryset = Household.objects.all()
    serializer_class = MinimalHouseholdSerializer

    def list(self, request):
        queryset = Household.objects.filter(members=request.user).all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class HousehostRetrieveApi(generics.RetrieveAPIView):
    queryset = Household.objects.all()
    serializer_class = HouseholdWithMembersSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "household_uuid"
    permission_classes = [permissions.CanAccessHousehold]
