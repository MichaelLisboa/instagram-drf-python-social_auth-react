import os

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from requests.exceptions import HTTPError
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import (AuthForbidden, AuthTokenError,
                                    MissingBackend)

from . import models
from .serializers import CelebsSerializer, ProfilesSerializer

User = get_user_model()
HOST_URL = settings.HOST_URL


class ProfileViewSet(ProtectedResourceView, viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ProfilesSerializer

    def get(self, request, *args, **kwargs):
        return request.user


class GetUserProfile(generics.RetrieveAPIView):

    serializer_class = ProfilesSerializer

    def get(self, request):

        if request.user.is_authenticated:
            serializer = ProfilesSerializer(request.user.profile)
        else:
            serializer = {
                "status": "failed",
                "message": "User not found"
            }
        return Response(serializer.data, status=200)


class CelebViewSet(viewsets.ModelViewSet):
    queryset = models.CelebModel.objects.all()
    serializer_class = CelebsSerializer


class ConvertToken(APIView):

    def post(self, request, format=None, **kwargs):

        params = {
            "grant_type": "convert_token",
            "client_id": os.environ['APP_CLIENT_ID'],
            "client_secret": os.environ['APP_CLIENT_SECRET'],
            "backend": "instagram",
            "token": self.request.data['token']
        }

        res = requests.post(
            url=f"{HOST_URL}auth/convert-token/",
            params=params
        )

        data = {"status": None}
        if res.ok:
            res = res.json()
            data.update({
                "status": "success",
                "access_token": res['access_token'],
                "refresh_token": res['refresh_token']
            })

        return Response(data, status=200)
