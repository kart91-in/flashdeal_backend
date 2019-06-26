from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, mixins, \
    UpdateAPIView, get_object_or_404, ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from flashdeal.contances import STATE_LIST
from flashdeal.models.vendor_models import Vendor
from flashdeal.serializers.vendor_serializers import VendorSerializer


class StateListAPI(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        response = [{'value': state[0], 'name': state[1]} for state in STATE_LIST]
        return Response({'states': response}, status=status.HTTP_200_OK)

