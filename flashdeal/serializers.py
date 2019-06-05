from django.contrib.auth import get_user_model
from rest_framework import serializers
from flashdeal.models.vendor_models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('user_id', 'name', 'email', 'gstin_number', 'phone', 'status')

    user_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=500)
    email = serializers.EmailField(required=True)
    gstin_number = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('user_id', 'name', 'email', 'gstin_number', 'phone', 'status')

    user_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=500)
    email = serializers.EmailField(required=True)
    gstin_number = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "email")

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user