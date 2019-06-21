from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from flashdeal.models import Order
from flashdeal.serializers.order_serializers import OrderSerializer


class OrderRetrieveUpdateDeleteAPI(RetrieveUpdateAPIView):

    permission_classes = (IsAdminUser, )
    serializer_class = OrderSerializer
    post_action = None

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs.get('pk'))


class OrderListCreateAPI(ListCreateAPIView):

    permission_classes = (IsAdminUser, )
    serializer_class = OrderSerializer
    queryset = Order.objects

