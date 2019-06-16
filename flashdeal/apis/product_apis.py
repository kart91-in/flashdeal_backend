from rest_framework import mixins
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from flashdeal.models import Product
from flashdeal.models.product_models import ProductColor
from flashdeal.serializers.product_serializers import ProductsSerializer, ProductColorSerializer


class ProductColorListAPI(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = ProductColor.objects
    serializer_class = ProductColorSerializer


class ProductSizeListAPI(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = ProductColor.objects
    serializer_class = ProductColorSerializer


class ProductListCreateAPI(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Product.objects.order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super().get_permissions()


class ProductDestroyUpdateAPI(mixins.DestroyModelMixin, RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get('pk'))

    def delete(self, request, *argv, **kwargs):
        return self.destroy(request, *argv, **kwargs)

