from rest_framework import serializers
from flashdeal.models import Catalog, Product
from flashdeal.serializers.product_serializers import ProductsSerializer
from flashdeal.serializers.vendor_serializers import VendorSerializer

class CurrentVendorDefault:
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user
        self.vendor = self.user.vendor

    def __call__(self):
        return self.vendor


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = ('id', 'name', 'description', 'vendor', 'vendor_id', 'status',
                  'products', 'product_ids', 'created_at')
        extra_kwargs = {
            'vendor_id': {'default': CurrentVendorDefault(), 'source': 'vendor'},
            'status': {'read_only': True, },
            'description': {'required': False, },
        }

    product_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Product.objects),
        allow_empty=False,
        write_only=True
    )

    products = ProductsSerializer(many=True, read_only=True)
    vendor = VendorSerializer(read_only=True)

    def create(self, validated_data):
        products = validated_data.pop('product_ids')
        validated_data['products'] = products
        return super().create(validated_data)

    def update(self, instance, validated_data):
        products = validated_data.pop('product_ids')
        validated_data['products'] = products
        return super().update(instance, validated_data)
