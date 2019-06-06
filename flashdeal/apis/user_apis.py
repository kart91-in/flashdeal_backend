from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, mixins
from flashdeal.serializers import UserSerializer


class UserRegisterAPI(CreateAPIView):
    model = get_user_model()
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer