from decimal import Decimal
from django.db import models
from core.models import BaseModel


class Product(BaseModel):

    vendor = models.ForeignKey('flashdeal.Vendor', on_delete=models.PROTECT,
                             related_name='products', related_query_name='product')
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    upper_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField('flashdeal.Image', blank=True, related_name='products',
                                    related_query_name='product')

    colors = models.ManyToManyField('ProductSize', blank=True, related_name='products',
                                    related_query_name='product')
    sizes = models.ManyToManyField('ProductColor', blank=True, related_name='products',
                                    related_query_name='product')

    def sale_percent(self):
        upper_price = self.get_upper_price()
        return (upper_price - self.sale_price) * Decimal(100.0) / upper_price

    def get_upper_price(self):
        if self.upper_price < self.sale_price or not self.upper_price:
            return self.sale_price
        return self.upper_price

    def image_url(self):
        image = self.images.first()
        if not image: return None
        return image.image.url

    def catalogs_list(self):
        if self.catalogs.exists():
            return ','.join(list(self.catalogs.values_list('name', flat=True)))
        return '--'


class ProductSize(BaseModel):

    name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)


class ProductColor(BaseModel):

    name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)
