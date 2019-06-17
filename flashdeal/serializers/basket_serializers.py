from rest_framework import serializers
from flashdeal.models import Basket, Product
from flashdeal.models.product_models import ProductVariant
from flashdeal.serializers.product_serializers import ProductsVariantSerializer


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('user_id', 'variant_id', 'product_variants')
        extra_kwargs = {
            'user_id': {'default': serializers.CurrentUserDefault(), 'source': 'user'},
        }

    product_variants = ProductsVariantSerializer(many=True, read_only=True)

    variant_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=ProductVariant.objects, required=True)

    def update(self, instance, validated_data):
        model = super().update(instance, validated_data)
        variant = validated_data.get('variant_id')
        model.product_variants.add(variant)
        return model

