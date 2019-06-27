from django.contrib.auth import get_user_model
from rest_framework import serializers

from flashdeal.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'phone', 'name', 'city', )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'date_joined', 'profile')

    profile = serializers.SerializerMethodField(source='get_profile_detail')

    def profile_detail(self, obj):
        if not hasattr(obj, 'profile'):
            return None
        return ProfileSerializer(obj.profile).data

class UserSerializer(serializers.Serializer):

    phone = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['phone'],
            email=validated_data['email'],
            is_active=False,
        )
        user.set_password(validated_data['phone'])
        UserProfile.objects.create(
            user=user,
            phone=validated_data['phone'],
            name=validated_data['phone'],
            city=validated_data['city'],
        )
        user.save()
        return user


