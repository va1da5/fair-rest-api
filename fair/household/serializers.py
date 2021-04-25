from rest_framework import serializers

from fair.core.serializers import UserSerializer

from .models import Household


class MinimalHouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ["uuid", "name"]


class HouseholdWithMembersSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Household
        fields = ["uuid", "name", "members"]
