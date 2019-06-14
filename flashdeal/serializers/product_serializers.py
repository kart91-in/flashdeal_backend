from rest_framework import serializers
from flashdeal.models import Product, Image


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('name', 'owner_id', 'url', )


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'sale_price', 'upper_price', 'images')

    images = ImagesSerializer(many=True)
