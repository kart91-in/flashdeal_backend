from rest_framework.generics import RetrieveUpdateAPIView, mixins
from rest_framework.permissions import IsAuthenticated

from flashdeal.serializers.order_serializers import OrderSerializer


class OrderRetrieveUpdateDeleteAPI(mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer
    post_action = None

    def post(self, request, *args, **kwargs):
        if self.post_action is not None:
            func = getattr(self, self.post_action)
            return func(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)


