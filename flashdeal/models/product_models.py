from django.db import models
from core.models import BaseModel
from flashdeal.models.static_file_models import Image
from flashdeal.models.vendor_models import Vendor


class Product(BaseModel):
    class Meta:
        app_label = "flashdeal"

    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,
                             related_name='products', related_query_name='product')
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    upper_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField(Image, related_name='products', related_query_name='product')
