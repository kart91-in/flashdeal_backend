from django.db import transaction
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, mixins, get_object_or_404, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from flashdeal.models import Payment
from flashdeal.serializers.payment_serializers import PaymentSerializer


class PaymentRetrieveAPI(RetrieveAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = PaymentSerializer

    def get_object(self):
        current_user = self.request.user
        kwargs = {} if current_user.is_superuser else {'user': current_user}
        return get_object_or_404(Payment, pk=self.kwargs.get('pk'), **kwargs)


class PaymentListCreateAPI(ListCreateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = PaymentSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)
