from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from flashdeal.models import FlashDeal
from flashdeal.serializers.flashdeal_serializers import FlashDealSerializer
from flashdeal.serializers.payment_serializers import PaymentSerializer


class FlashDealListCreateAPI(ListCreateAPIView):
    queryset = FlashDeal.objects
    permission_classes = (AllowAny, )
    serializer_class = FlashDealSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return (IsAuthenticated(), )
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            raise ParseError('Input data invalid')
        except ValidationError as e:
            raise ParseError(e.message)


class FlashDealRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FlashDealSerializer

    def get_object(self):
        return get_object_or_404(FlashDeal, pk=self.kwargs.get('pk'))

    def put(self, request, *args, **kwargs):
        try:
            return super().put(request, *args, **kwargs)
        except IntegrityError:
            raise ParseError('Input data invalid')
        except ValidationError as e:
            raise ParseError(e.detail)
