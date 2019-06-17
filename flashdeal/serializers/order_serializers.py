from rest_framework import serializers
from flashdeal.models import Order, Basket
from flashdeal.serializers.product_serializers import ProductsVariantSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total_price',

                  'customer_name', 'customer_phone', 'customer_address', 'address_type',
                  'pin_code', 'c_city', 'c_state', 'alternate_customer_contact',

                  'product_variants',
                  )
        extra_kwargs = {
            'user': {'read_only': True}
        }

    status = serializers.CharField(read_only=True, source='status_text')
    product_variants = ProductsVariantSerializer(many=True, read_only=True)

    def validate(self, data):
        basket, _ = Basket.objects.get_or_create(user=self.context['request'].user)
        self.basket = basket
        if basket.product_variants.count() == 0:
            raise serializers.ValidationError("Basket is empty")
        return data

    def create(self, validated_data):
        validated_data = {
            'user': self.basket.user,
            'product_variants': self.basket.product_variants.all(),
            **validated_data,
        }
        return super().create(validated_data)

