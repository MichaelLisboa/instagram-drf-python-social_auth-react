import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from .serializers import (MembershipSerializer, SubscriptionSerializer,
                          UserMembershipSerializer)

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET


class UserMembershipsViewSet(viewsets.ModelViewSet):
    queryset = models.UserMembership.objects.all()
    serializer_class = UserMembershipSerializer


class MembershipsViewSet(viewsets.ModelViewSet):
    queryset = models.Membership.objects.all()
    serializer_class = MembershipSerializer


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = models.Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SocialSubscription(APIView):

    def get(self, request, pk=None, format=None, **kwargs):

        user = request.user
        selected_membership = (
                models.Membership
                .objects
                .get(membership_type='free')
                )

        _cus = {
            "email": user.email,
            "description": user.username
        }
        cus = stripe.Customer.create(**_cus)
        cus.save()

        _sub = {
                "items": [{'plan': selected_membership.stripe_plan_id}],
                "customer": cus.id
            }
        subscription = stripe.Subscription.create(**_sub)

        user_membership, created = (
                models
                .UserMembership
                .objects
                .get_or_create(user=user)
            )
        user_membership.membership = selected_membership
        user_membership.stripe_customer_id = cus.id
        user_membership.save()
        sub, created = (
            models.Subscription.objects.get_or_create(
                user_membership=user_membership)
        )
        sub.stripe_subscription_id = subscription.id
        sub.active = True
        sub.save()
        serializer = MembershipSerializer(selected_membership)

        return Response(serializer.data, status=200)
