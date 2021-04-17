from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import serializers


class UserViewSet(viewsets.ModelViewSet):
    class UserSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = User
            fields = ["url", "username", "email"]

    queryset = User.objects.all()
    serializer_class = UserSerializer
