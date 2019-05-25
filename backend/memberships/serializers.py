from rest_framework import serializers
from .models import Membership, UserMembership, Subscription


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ("__all__")


class UserMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMembership
        fields = ("__all__")


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ("__all__")
