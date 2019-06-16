from django.contrib.auth import get_user_model
from rest_framework import serializers

from flashdeal.models import UserProfile


class UserSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['phone'],
            is_active=False,
        )
        UserProfile.objects.create(user=user, phone=validated_data['phone'])
        return user


