from django.db import transaction
from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from flashdeal.serializers.payment_serializers import PaymentSerializer


class PaymentRetrieveCreateDeleteAPI(mixins.CreateModelMixin,
                                     RetrieveDestroyAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

