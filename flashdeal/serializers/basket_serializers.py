from rest_framework import serializers
from flashdeal.models import Basket, Product
from flashdeal.serializers.product_serializers import ProductsSerializer


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('user_id', 'product_id', 'products')

    user_id = serializers.CharField(read_only=True)
    products = ProductsSerializer(many=True, read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Product.objects, required=True)

    def update(self, instance, validated_data):
        model = super().update(instance, validated_data)
        product = validated_data.get('product_id')
        model.products.add(product)
        return model

