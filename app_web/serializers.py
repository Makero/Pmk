from rest_framework import serializers
from app_web import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = "__all__"
        # extra_kwargs = {'password': {'write_only': True}}


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Article
        fields = "__all__"


class MoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Mood
        fields = "__all__"
