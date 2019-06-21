from rest_framework import mixins
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from flashdeal.models import Product, Catalog
from flashdeal.serializers.catalog_serializers import CatalogSerializer


class CatalogListCreateAPI(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CatalogSerializer

    def get_queryset(self):
        return Catalog.objects.order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny, )
        return super().get_permissions()


class CatalogDestroyUpdateAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CatalogSerializer

    def get_object(self):
        return Catalog.objects.get(pk=self.kwargs.get('pk'))

