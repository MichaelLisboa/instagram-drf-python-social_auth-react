from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.response import Response

from . import models
from .serializers import (ProfilesSerializer, CelebsSerializer)

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ProfilesSerializer


class CelebViewSet(viewsets.ModelViewSet):
    queryset = models.CelebModel.objects.all()
    serializer_class = CelebsSerializer
