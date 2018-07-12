from rest_framework import serializers
from app_web import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = "__all__"
        # extra_kwargs = {'password': {'write_only': True}}


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Token
        fields = "__all__"
