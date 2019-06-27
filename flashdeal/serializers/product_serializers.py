import json

from django.db import transaction
from rest_framework import serializers
from flashdeal.models import Product, Image
from flashdeal.models.product_models import ProductVariant, ProductColor, ProductSize


class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductColor
        fields = ('id', 'name', 'value', )


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('id', 'name', 'value',)


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'owner_id', 'url', )


class ProductSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id' ,'name', 'description', 'sale_price', 'upper_price', 'images', 'created_at' )

    images = ImagesSerializer(many=True, required=False)


class ProductsVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = ('id', 'stock', 'color_id', 'size_id', 'upper_price',
                  'sale_price', 'product_id', 'color', 'size', 'product')
        extra_kwargs = {
            'upper_price': {'required': False},
            'stock': {'required': False, },
            'color_id': {'source': 'color'},
            'size_id': {'source': 'size'},
            'product_id': {'source': 'product'},
        }

    def __init__(self, instance=None, **kwargs):
        if not kwargs.pop('show_product', True):
            del self.fields['product']
        super().__init__(instance=instance, **kwargs)

    product = ProductSimpleSerializer(read_only=True)
    color = ProductColorSerializer(read_only=True)
    size = ProductSizeSerializer(read_only=True)


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id' ,'name', 'description', 'sale_price', 'upper_price', 'images', 'variants',
                  'image_files', 'product_variants', 'created_at')
        extra_kwargs = {
            'upper_price': {'required': False},
            'images': {'required': False,}
        }

    images = ImagesSerializer(many=True, required=False)
    image_files = serializers.ListField(write_only=True,
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False)
    )
    product_variants = ProductsVariantSerializer(many=True, source='variants',
                                                 read_only=True, show_product=False)
    variants = serializers.JSONField(write_only=True)

    @transaction.atomic
    def create(self, validated_data):
        vendor = self.context['request'].user.vendor
        input_data = {**validated_data, 'vendor': vendor}

        image_files = input_data.pop('image_files')
        variants = input_data.pop('variants')

        instance = super().create(input_data)

        for image_file in image_files:
            instance.images.create(image=image_file, owner=vendor.user )
        variants = [{
            **variant,
            'product_id': instance.pk,
            'upper_price': instance.upper_price,
            'sale_price': instance.sale_price,
        } for variant in variants]

        variants = ProductsVariantSerializer(data=variants, many=True)
        variants.is_valid(True)
        variant_objs = variants.save()
        instance.variants.set(variant_objs)

        return instance
