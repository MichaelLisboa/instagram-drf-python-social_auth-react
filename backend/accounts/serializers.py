from rest_framework import serializers
from .models import Profile, CelebModel


class ProfilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("__all__")


class CelebsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CelebModel
        fields = ("__all__")
