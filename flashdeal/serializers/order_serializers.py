from rest_framework import serializers
from flashdeal.models import Order, Basket
from flashdeal.serializers.product_serializers import ProductsSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user_id', 'products', 'name', 'address', 'phone',
                  'city', 'pin_code', 'alternate_contact', 'status',
                  'total_price')

    status = serializers.CharField(read_only=True, source='status_text')
    products = ProductsSerializer(many=True, read_only=True)

    def validate(self, data):
        basket, _ = Basket.objects.get_or_create(user=self.context['request'].user)
        self.basket = basket
        if basket.products.count() == 0:
            raise serializers.ValidationError("Basket is empty")
        return data

    def create(self, validated_data):
        validated_data = {
            'user': self.basket.user,
            'products': self.basket.products.all(),
            **validated_data,
        }
        return super().create(validated_data)

