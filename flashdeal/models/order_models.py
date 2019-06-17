from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Sum

from core.models import BaseModel
from flashdeal.contances import STATE_LIST


class Basket(BaseModel):

    product_variants = models.ManyToManyField('flashdeal.ProductVariant')
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
        (STATUS_PAYMENT, 'Paid and processing'),
        (STATUS_VERIFIED, 'Vendor Received'),
        (STATUS_SHIPPED, 'Is Shipping'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELED, 'Canceled'),
    )

    TYPE_HOME_ADDRESS = 0
    TYPE_HOME_OFFICE = 1

    CUSTOMER_ADDRESS_TYPE = (
        (TYPE_HOME_ADDRESS, 'home'),
        (TYPE_HOME_OFFICE, 'office'),
    )

    product_variant = models.ManyToManyField('flashdeal.ProductVariant', blank=False)

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', related_query_name='order')

    payment = models.OneToOneField('flashdeal.Payment', on_delete=models.PROTECT, related_name='order', null=True, blank=True)
    tracking = models.OneToOneField('flashdeal.Tracking', on_delete=models.PROTECT, null=True, blank=True)

    status = models.PositiveSmallIntegerField(default=STATUS[0][0], choices=STATUS)

    customer_name = models.CharField(max_length=500)
    customer_phone = models.CharField(max_length=500)
    customer_address = models.CharField(max_length=500)
    address_type = models.CharField(max_length=500, default=TYPE_HOME_ADDRESS, choices=CUSTOMER_ADDRESS_TYPE)
    city = models.CharField(max_length=500)
    pin_code = models.CharField(max_length=500)
    c_city = models.CharField(max_length=500)
    c_state = models.CharField(max_length=500, choices=STATE_LIST)
    alternate_customer_contact = models.CharField(max_length=500, blank=True, null=True)

    delivery_info = models.OneToOneField('flashdeal.DeliveryInfo', null=True, blank=True, on_delete=models.PROTECT)


    def __str__(self):
        return 'Order %s: %s' % (self.id, self.customer_name)

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


class DeliveryInfo(BaseModel):

    awb_number = models.CharField(max_length=500, primary_key=True)

    actual_weight = models.PositiveIntegerField(default=0)
    volumetric_weight = models.PositiveIntegerField(default=0)
    pincode = models.PositiveIntegerField(default=0)

    pickup_address = models.CharField(max_length=500)
    pickup_address_pincode = models.PositiveIntegerField(default=0)

    rto_name = models.CharField(max_length=500)
    rto_city = models.CharField(max_length=500)
    rto_state = models.CharField(max_length=500, choices=STATE_LIST)
    rto_contact_no = models.CharField(max_length=500, blank=True, null=True)
    rto_address = models.CharField(max_length=500, blank=True, null=True)
    rto_pincode = models.PositiveIntegerField(default=0)


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
