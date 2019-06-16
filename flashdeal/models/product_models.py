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

    sizes = models.ManyToManyField('ProductSize', blank=True, related_name='products',
                                    related_query_name='product', through='ProductVariant')
    colors = models.ManyToManyField('ProductColor', blank=True, related_name='products',
                                    related_query_name='product', through='ProductVariant')

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


class ProductVariant(BaseModel):

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='variants', related_query_name='variant')
    size = models.ForeignKey('ProductSize', on_delete=models.CASCADE)
    color = models.ForeignKey('ProductColor', on_delete=models.CASCADE)

    upper_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveSmallIntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.upper_price:
            self.upper_price = self.sale_price
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class ProductSize(BaseModel):

    name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)


class ProductColor(BaseModel):

    name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)
