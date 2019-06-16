from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from flashdeal.otp_service import verify_otp, send_otp_message, resend_otp_message
from flashdeal.serializers.user_serializers import UserSerializer


class UserRegisterAPI(CreateAPIView):

    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        send_otp_result = send_otp_message(request.data.get('phone'))
        if send_otp_result.get('type') != 'success':
            transaction.rollback()
            return Response(send_otp_result, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class UserResendOtpAPI(APIView):

    def post(self, request, *args, **kwargs):
        resend_otp_result = resend_otp_message(request.data.get('phone'))
        if resend_otp_result.get('type') != 'success':
            return Response(resend_otp_result, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class UserTokenAPI(APIView):

    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        user_phone = request.data.get('phone')
        user = User.objects.filter(username=user_phone, is_active=False).first()

        verify_result = verify_otp(user_phone, otp)

        if verify_result.get('type') != 'success':
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token }, status=status.HTTP_202_ACCEPTED)


