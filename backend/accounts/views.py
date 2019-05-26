from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.response import Response

from django.contrib.auth import login

from social_django.utils import psa

from . import models
from .serializers import (ProfilesSerializer, CelebsSerializer)

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ProfilesSerializer


class CelebViewSet(viewsets.ModelViewSet):
    queryset = models.CelebModel.objects.all()
    serializer_class = CelebsSerializer


# Define an URL entry to point to this view, call it passing the
# access_token parameter like ?access_token=<token>. The URL entry must
# contain the backend, like this:
#
#   url(r'^register-by-token/(?P<backend>[^/]+)/$', 'register_by_access_token')


@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.GET.get('access_token')
    user = request.backend.do_auth(token)
    if user:
        login(request, user)
        return 'OK'
    else:
        return 'ERROR'
