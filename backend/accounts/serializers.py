from rest_framework import serializers

from .models import CelebModel, Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    email = serializers.CharField(allow_blank=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'last_login',)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['email'] = self.validated_data.get('email', '')
        return data_dict


class ProfilesSerializer(serializers.ModelSerializer):

    # user = UserSerializer(many=False, read_only=True)

    first_name = serializers.CharField(
            source="user.first_name", allow_blank=True, required=False)
    last_name = serializers.CharField(
            source="user.last_name", allow_blank=True, required=False)
    email = serializers.CharField(
            source="user.email", allow_blank=True, required=False)
    date_joined = serializers.DateTimeField(
            source="user.date_joined", read_only=True)
    last_login = serializers.DateTimeField(
            source="user.last_login", allow_null=True)

    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'email',
                  'profile_pic', 'slug', 'email_confirmed',
                  'date_joined', 'last_login',)


class CelebsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CelebModel
        fields = ("__all__")


class SocialSerializer(serializers.Serializer):

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True)
