import requests
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


class CityListAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        resp = requests.get('https://raw.githubusercontent.com/nshntarora/Indian-Cities-JSON/master/cities.json')
        if not resp.ok:
            return Response({'error': 'Service error'},status=status.HTTP_400_BAD_REQUEST)
        state = request.GET.get('state')
        if not state:
            return Response(resp.json(), status=status.HTTP_200_OK)
        filtered = filter(lambda item: item.get('state') == state, resp.json())
        return Response(filtered, status=status.HTTP_200_OK)
