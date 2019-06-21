from rest_framework import serializers
from flashdeal.models import FlashDeal
from flashdeal.serializers.catalog_serializers import CatalogSerializer


class FlashDealSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlashDeal
        fields = ('id', 'catalog_id', 'name', 'catalog', 'start_time', 'end_time', )
        extra_kwargs = {
            'end_time': {'required': False, },
            'catalog': {'required': False, 'read_only': True},
        }

    catalog = CatalogSerializer(read_only=True)
    catalog_id = serializers.IntegerField(write_only=True)
