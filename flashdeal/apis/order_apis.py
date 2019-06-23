from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from flashdeal.models import Order, ReturnOrder
from flashdeal.serializers.order_serializers import OrderSerializer, ReturnOrderSerializer, DeliveryInfoSerializer


class OrderRetrieveUpdateDeleteAPI(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer
    post_action = None

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs.get('pk'))


class OrderListCreateAPI(ListCreateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer
    queryset = Order.objects


class DeliveryInfoCreateAPI(CreateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = DeliveryInfoSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['data'] = {**kwargs['data'], 'order': self.kwargs.get('pk')}
        return super().get_serializer(*args, data=kwargs['data'])


class SendOrderToDeliveryAPI(APIView):

    permission_classes = (IsAdminUser, )

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        resp = order.delivery_info.send_to_delivery()
        if resp.ok:
            return Response(status=status.HTTP_200_OK)
        return Response(resp.json(), status=resp.status_code)


class OrderResendCreateAPI(ListCreateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = ReturnOrderSerializer
    queryset = ReturnOrder.objects

    def get_serializer(self, *args, **kwargs):
        obj = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        kwargs['data'] = {
            **kwargs['data'],
            'order_id': obj.id,
            'total_amount': obj.declared_total_price,
            'price': obj.total_price,
        }
        return super().get_serializer(*args, **kwargs)


class ReturnOrderAPI(APIView):

    permission_classes = (IsAdminUser, )

    def post(self, request, *args, **kwargs):
        return_request = get_object_or_404(ReturnOrder, pk=self.kwargs.get('pk'))
        resp = return_request.send_to_delivery()
        if resp.ok:
            return Response(status=status.HTTP_200_OK)
        return Response(resp.json(), status=resp.status_code)
