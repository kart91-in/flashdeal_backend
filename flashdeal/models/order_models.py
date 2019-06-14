from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Sum

from core.models import BaseModel


class Basket(BaseModel):

    products = models.ManyToManyField('flashdeal.Product')
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='basket',
                             related_query_name='basket', primary_key=True)


class Order(BaseModel):

    STATUS_DRAFT = 0
    STATUS_PAYMENT = 1
    STATUS_VERIFIED = 2
    STATUS_SHIPPED = 3
    STATUS_DELIVERED = 4
    STATUS_CANCELED = 5

    STATUS = (
        (STATUS_DRAFT, 'Just created'),
        (STATUS_PAYMENT, 'Paid'),
        (STATUS_VERIFIED, 'Vendor Received'),
        (STATUS_SHIPPED, 'Is Shipping'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELED, 'Canceled'),
    )

    products = models.ManyToManyField('flashdeal.Product', blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', related_query_name='order')

    payment = models.OneToOneField('flashdeal.Payment', on_delete=models.PROTECT, related_name='order', null=True, blank=True)
    tracking = models.OneToOneField('flashdeal.Tracking', on_delete=models.PROTECT, null=True, blank=True)

    status = models.PositiveSmallIntegerField(default=STATUS[0][0], choices=STATUS)

    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    pin_code = models.CharField(max_length=500)
    alternate_contact = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return 'Order %s: %s' % (self.id, self.name)

    @property
    def status_text(self):
        return self.get_status_display()

    @property
    def total_price(self):
        return self.products.all().aggregate(total=Sum('sale_price'))['total']

    def add_payment(self, payment):
        if self.payment:
            return
        self.payment = payment
        self.status = self.STATUS_PAYMENT
        self.save()


class Tracking(BaseModel):

    tracking_id = models.CharField(max_length=500, unique=True, primary_key=True)
    tracking_type = models.CharField(max_length=500)
    meta = JSONField(default=dict)


class Payment(BaseModel):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments', related_query_name='payment')
    transaction_id = models.CharField(max_length=500, unique=True)
    gateway_order_id = models.CharField(max_length=500, unique=True)
    gateway = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    meta = JSONField(default=dict)
