from rest_framework import serializers
from flashdeal.models import Basket, Product, ProductVariantBasket
from flashdeal.models.product_models import ProductVariant
from flashdeal.serializers.product_serializers import ProductsVariantSerializer


class BasketPurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantBasket
        fields = ('id', 'product_variant', 'amount', 'basket_id')

    product_variant = ProductsVariantSerializer(read_only=True)


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('user_id', 'variant_id', 'purchases')
        extra_kwargs = {
            'user_id': {'default': serializers.CurrentUserDefault(), 'source': 'user'},
        }

    purchases = BasketPurchasesSerializer(many=True, read_only=True)

    variant_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=ProductVariant.objects, required=True)

    def update(self, instance, validated_data):
        variant = validated_data.get('variant_id')
        instance.add_product_variant(variant)
        return instance

