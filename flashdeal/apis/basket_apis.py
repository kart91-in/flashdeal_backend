from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from flashdeal.models import Basket, Product
from flashdeal.serializers.basket_serializers import BasketSerializer


class BasketRetrieveUpdateDeleteAPI(mixins.DestroyModelMixin, RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = BasketSerializer
    remove_product = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_object(self):
        user = self.request.user
        basket, _ = Basket.objects.get_or_create(user=user)
        return basket

    def put(self, request, *args, **kwargs):
        if self.remove_product:
            # Remove product from basket
            obj = self.get_object()
            product_id = request.data.get('product_id')
            product_remove = Product.objects.filter(pk=product_id).first()
            if not product_remove:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            obj.products.remove(product_remove)
            return Response(self.get_serializer(obj).data)
        return self.update(request, *args, **kwargs)
