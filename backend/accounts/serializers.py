from rest_framework import serializers

from .models import CelebModel, Profile


class ProfilesSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
            source="user.first_name", allow_blank=True, required=False)
    last_name = serializers.CharField(
            source="user.last_name", allow_blank=True, required=False)
    email = serializers.CharField(
            source="user.email", allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ("__all__")


class CelebsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CelebModel
        fields = ("__all__")


class SocialSerializer(serializers.Serializer):

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True)
