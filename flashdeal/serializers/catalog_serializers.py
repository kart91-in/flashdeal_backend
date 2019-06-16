from rest_framework import serializers
from flashdeal.models import Catalog
from flashdeal.serializers.product_serializers import ProductsSerializer
from flashdeal.serializers.vendor_serializers import VendorSerializer


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = ('id', 'name', 'description', 'vendor', 'status', 'products')
        extra_kwargs = {
            'status': {'read_only': True, },
            'description': {'required': False, },
        }

    products = ProductsSerializer(many=True)
    vendor = VendorSerializer()
