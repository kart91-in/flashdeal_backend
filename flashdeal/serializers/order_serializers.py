from rest_framework import serializers
from flashdeal.models import Order, Basket, ProductVariantOrder
from flashdeal.serializers.product_serializers import ProductsVariantSerializer


class OrderPurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantOrder
        fields = ('id', 'product_variant', 'amount', 'order_id')

    product_variant = ProductsVariantSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total_price',

                  'customer_name', 'customer_phone', 'customer_address', 'address_type',
                  'pin_code', 'c_city', 'c_state', 'alternate_customer_contact',

                  'purchases',
                  )
        extra_kwargs = {
            'user': {'read_only': True}
        }

    status = serializers.CharField(read_only=True, source='status_text')
    purchases = OrderPurchasesSerializer(many=True, read_only=True)

    def validate(self, data):
        basket, _ = Basket.objects.get_or_create(user=self.context['request'].user)
        self.basket = basket
        if basket.purchases.count() == 0:
            raise serializers.ValidationError("Basket is empty")
        return data

    def create(self, validated_data):
        validated_data = {
            'user': self.basket.user,
            **validated_data,
        }
        order = super().create(validated_data)
        for purchase in self.basket.purchases.all():
            order.purchases.create(
                product_variant=purchase.product_variant,
                amount=purchase.amount,
            )

        return order