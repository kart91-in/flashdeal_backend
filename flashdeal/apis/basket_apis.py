from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from flashdeal.models import Basket, Product
from flashdeal.models.product_models import ProductVariant
from flashdeal.serializers.basket_serializers import BasketSerializer


class BasketRetrieveUpdateDeleteAPI(mixins.DestroyModelMixin, RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = BasketSerializer
    remove_product = False

    def get_object(self):
        user = self.request.user
        basket, _ = Basket.objects.get_or_create(user=user)
        return basket

    def put(self, request, *args, **kwargs):
        if self.remove_product:
            # Remove product from basket
            obj = self.get_object()
            variant_id = request.data.get('variant_id')
            variant_remove = ProductVariant.objects.filter(pk=variant_id).first()
            if not variant_remove:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            obj.product_variants.remove(variant_remove)
            return Response(self.get_serializer(obj).data)
        return self.update(request, *args, **kwargs)
