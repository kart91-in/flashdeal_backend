from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import mixins, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from flashdeal.models.vendor_models import Vendor
from flashdeal.serializers import VendorSerializer, UserSerializer


class VendorRetrieveUpdateCreateAPI(mixins.CreateModelMixin, RetrieveUpdateAPIView):

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserRegisterAPI(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer