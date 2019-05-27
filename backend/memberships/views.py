from django.contrib.auth import get_user_model
from rest_framework import viewsets

from . import models
from .serializers import (MembershipSerializer, SubscriptionSerializer,
                          UserMembershipSerializer)

User = get_user_model()


class UserMembershipsViewSet(viewsets.ModelViewSet):
    queryset = models.UserMembership.objects.all()
    serializer_class = UserMembershipSerializer


class MembershipsViewSet(viewsets.ModelViewSet):
    queryset = models.Membership.objects.all()
    serializer_class = MembershipSerializer


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = models.Subscription.objects.all()
    serializer_class = SubscriptionSerializer
