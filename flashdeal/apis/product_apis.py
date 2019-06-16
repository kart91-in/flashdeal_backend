from rest_framework import mixins
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from flashdeal.models import Product
from flashdeal.serializers.product_serializers import ProductsSerializer


class ProductCreateAPI(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer


class ProductUpdateAPI(mixins.DestroyModelMixin, UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer

    def get_object(self):
        return Product.objects.get(pk=self.kwargs.get('pk'))

    def delete(self, request, *argv, **kwargs):
        return self.destroy(request, *argv, **kwargs)

