from rest_framework import serializers

from flashdeal.models import Order, Payment
from flashdeal.models.vendor_models import Vendor


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user_id', 'transaction_id', 'gateway_order_id', 'gateway',
                  'created_at' ,'amount', 'meta', 'order', 'order_id')

    order_id = serializers.IntegerField(required=False, read_only=True, source='order.id')
    user_id = serializers.IntegerField(required=False)
    transaction_id = serializers.CharField(max_length=500)
    gateway_order_id = serializers.CharField(max_length=500)
    gateway = serializers.CharField(max_length=500)
    amount = serializers.DecimalField(decimal_places=2, max_digits=5)
    meta = serializers.JSONField(write_only=True, required=False)

    order = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Order.objects, write_only=True)

    def create(self, validated_data):
        validated_data = {
            'user_id': self.context['request'].user.id,
            **validated_data,
        }
        order = validated_data.pop('order')
        instance = super().create(validated_data)
        order.add_payment(instance)
        return instance
