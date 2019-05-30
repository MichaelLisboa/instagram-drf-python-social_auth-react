import os

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import (AuthForbidden, AuthTokenError,
                                    MissingBackend)

from . import models
from .serializers import CelebsSerializer, ProfilesSerializer
from .tokens import account_activation_token

User = get_user_model()
HOST_URL = settings.HOST_URL


class ProfileViewSet(ProtectedResourceView, viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ProfilesSerializer

    def get(self, request, *args, **kwargs):
        return request.user

    def partial_update(self, request, pk=None):
        data = request.data
        user = request.user
        instance = self.queryset.filter(user_id=pk).first()

        user.email = data['email']
        user.save()

        serializer = ProfilesSerializer(instance)
        current_site = get_current_site(request)
        subject = (
            'Hello from influen$e! Please confirm your email address.'
        )
        message = render_to_string(
            'templates/emails/email_change_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        to_email = data['email']
        email = EmailMessage(
            subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()

        return Response(serializer.data, status=200)


class GetUserProfile(ProtectedResourceView, generics.RetrieveAPIView):

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
            url=f"{HOST_URL}api/auth/oauth/convert-token/",
            params=params
        )

        data = {"status": None}
        if res.ok:
            res = res.json()
            print("RES", request)
            data.update({
                "status": "success",
                # "user_id":
                "access_token": res['access_token'],
                "refresh_token": res['refresh_token']
            })

        return Response(data, status=200)


class UpdateEmail(ProtectedResourceView, APIView):
    queryset = models.Profile.objects.all()
    serializer_class = ProfilesSerializer

    def post(self, request, pk=None):
        data = request.data
        user = request.user
        instance = self.queryset.filter(user_id=pk).first()

        user.email = data['email']
        user.save()

        serializer = ProfilesSerializer(instance)
        subject = (
            'Hello from influen$e! Please confirm your email address.'
        )
        message = render_to_string(
            'templates/emails/email_change_email.html',
            {
                'user': user,
                'domain': '127.0.0.1:3000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        to_email = data['email']
        email = EmailMessage(
            subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()

        return Response(serializer.data, status=200)


class ActivateEmail(APIView):

    def get(self, request, uidb64, token, format=None, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if (user is not None
                and account_activation_token.check_token(user, token)):
            # user.is_active = True
            # user.save()
            user.profile.email_confirmed = True
            user.profile.save()
            login(
                request,
                user,
                backend='django.contrib.auth.backends.ModelBackend'
            )
            profile = ProfilesSerializer(user.profile)
            data = {
                    "status": "success",
                    "user": profile.data,
                    "message": f"Your account is activated @{user.username}!"
            }
            return Response(data, status=200)
        else:
            data = {
                    "status": "failed",
                    "message": "Sorry that token is invalid :-("
            }
            return Response(data, status=200)
