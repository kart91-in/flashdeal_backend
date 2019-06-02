from decimal import Decimal

from django.db import models
from core.models import BaseModel
from flashdeal.models.static_file_models import Image
from flashdeal.models.vendor_models import Vendor


class Product(BaseModel):

    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,
                             related_name='products', related_query_name='product')
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    upper_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField(Image, blank=True, related_name='products', related_query_name='product')

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