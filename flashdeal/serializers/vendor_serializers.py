from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated

from flashdeal.models.vendor_models import Vendor
from flashdeal.serializers.product_serializers import ImagesSerializer


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('pk', 'user_id', 'name', 'email', 'gstin_number', 'address',
                  'phone', 'status', 'state', 'status',
                  'username', 'password', 'images', 'created_at')
        extra_kwargs = {
            'user_id': {'default': serializers.CurrentUserDefault(), 'source': 'user'},
        }

    images = ImagesSerializer(many=True, read_only=True,)
    status = serializers.SerializerMethodField(read_only=True, )
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)

    def get_status(self, obj):
        return obj.get_status_display()

    def save(self, **kwargs):
        username = self.validated_data.pop('username', None)
        password = self.validated_data.pop('password', None)
        if username and password:
            user, created = User.objects.get_or_create(
                username=username, email=self.validated_data['email'])
            if not created:
                user.set_password(password)
            self.validated_data['user_id'] = user.id
        elif not self.context['request'].user:
            raise NotAuthenticated('No user info found')
        return super().save(**kwargs)

