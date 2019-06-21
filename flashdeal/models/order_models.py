from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.db.models import Sum

from core.models import BaseModel
from flashdeal.contances import STATE_LIST
from flashdeal.delivery_service import send_forward_request


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

    TYPE_HOME_ADDRESS = 'home'
    TYPE_HOME_OFFICE = 'office'

    CUSTOMER_ADDRESS_TYPE = (
        (TYPE_HOME_ADDRESS, 'home'),
        (TYPE_HOME_OFFICE, 'office'),
    )

    product_variants = models.ManyToManyField('flashdeal.ProductVariant', blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', related_query_name='order')
    payment = models.OneToOneField('flashdeal.Payment', on_delete=models.PROTECT, related_name='order', null=True, blank=True)
    return_order = models.OneToOneField('flashdeal.ReturnOrder', on_delete=models.PROTECT, related_name='order', null=True, blank=True)

    status = models.PositiveSmallIntegerField(default=STATUS[0][0], choices=STATUS)

    customer_name = models.CharField(max_length=500)
    customer_phone = models.CharField(max_length=500)
    customer_address = models.CharField(max_length=500)
    address_type = models.CharField(max_length=500, default=TYPE_HOME_ADDRESS, choices=CUSTOMER_ADDRESS_TYPE)
    pin_code = models.CharField(max_length=6)
    c_city = models.CharField(max_length=500)
    c_state = models.CharField(max_length=500, choices=STATE_LIST)
    alternate_customer_contact = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return 'Order %s: %s' % (self.id, self.customer_name)

    @property
    def status_text(self):
        return self.get_status_display()

    @property
    def total_price(self):
        return self.product_variants.all().aggregate(total=Sum('sale_price'))['total']

    @property
    def declared_total_price(self):
        return self.product_variants.all().aggregate(total=Sum('upper_price'))['total']

    def add_payment(self, payment):
        if self.payment:
            return
        self.payment = payment
        self.status = self.STATUS_PAYMENT
        self.save()

    def gen_delivery_request_params(self):
        delivery_info = self.delivery_info

        total_price = float(self.total_price)
        skus_attributes = [v.skus_attributes() for v in self.product_variants.all()]
        return {
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_address": self.customer_address,
            "address_type": self.address_type,
            "c_city": self.c_city,
            "c_state": self.c_state,
            "alternate_customer_contact": self.alternate_customer_contact,

            "declared_value": float(self.declared_total_price),
            "total_amount": total_price,
            "order_service": "NDD",
            "deliver_type": "Prepaid",
            "cod_amount": 0,
            'client_order_id': self.id,
            'awb_number': delivery_info.awb_number,
            'actual_weight': delivery_info.actual_weight,
            'volumetric_weight': delivery_info.volumetric_weight,
            'pincode': delivery_info.pincode,
            'rto_attributes': {
                "name": delivery_info.rto_name,
                "city": delivery_info.rto_city,
                "state": delivery_info.rto_state,
                "contact_no": delivery_info.rto_contact_no,
                "address": delivery_info.rto_address,
                "pincode": delivery_info.rto_pincode
            },
            'pickup_address_attributes': {
                'address': delivery_info.pickup_address,
                'pincode': delivery_info.pickup_address_pincode,
            },
            'rto_name': delivery_info.pickup_address_pincode,
            'skus_attributes': skus_attributes
        }



class DeliveryInfo(BaseModel):
    STATUS_NOT_SEND = 0
    STATUS_SENT_SUCCESS = 1
    STATUS_SENT_FAILED = 2

    STATUS = (
        (STATUS_NOT_SEND, 'not_send'),
        (STATUS_SENT_SUCCESS, 'success'),
        (STATUS_SENT_FAILED, 'failed'),
    )

    order = models.OneToOneField('flashdeal.Order', on_delete=models.PROTECT, related_name='delivery_info',)

    awb_number = models.CharField(max_length=500, null=True, blank=True, help_text='Will get one form AWB number data if not specific')

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

    status = models.PositiveIntegerField(default=STATUS_NOT_SEND, choices=STATUS)

    meta = JSONField(default=dict)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
            return

        awb_number = AWBNumber.objects.filter(is_used=False).order_by().first()
        if not awb_number and not self.awb_number:
            self.status = DeliveryInfo.STATUS_NOT_SEND
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
            return

        self.awb_number = self.awb_number or awb_number.value
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        self.order.delivery_info = self
        self.order.status = Order.STATUS_VERIFIED
        self.order.save()
        awb_number.is_used = True
        awb_number.save()
        self.send_to_delivery()

    def send_to_delivery(self):
        resp = send_forward_request(self.order.gen_delivery_request_params())
        if resp.get('message') != 'Success':
            self.status = DeliveryInfo.STATUS_SENT_FAILED
            if resp.get('message') == 'Invalid AWB Number. Existing order found with given awb number':
                AWBNumber.objects.filter(value=self.awb_number).update(is_used=True)
        else:
            self.status = DeliveryInfo.STATUS_SENT_SUCCESS
        self.meta = resp
        self.save()


class Tracking(BaseModel):

    tracking_id = models.CharField(max_length=500, unique=True, primary_key=True)
    tracking_type = models.CharField(max_length=500)
    meta = JSONField(default=dict)


class AWBNumber(BaseModel):

    value = models.CharField(max_length=500, unique=True)
    is_used = models.BooleanField(default=False)


class Payment(BaseModel):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments', related_query_name='payment')
    transaction_id = models.CharField(max_length=500, unique=True)
    gateway_order_id = models.CharField(max_length=500, unique=True)
    gateway = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    meta = JSONField(default=dict)


class ReturnOrder(BaseModel):

    warehouse_name = models.CharField(max_length=500)
    warehouse_address = models.CharField(max_length=500)
    destination_pincode = models.CharField(max_length=500)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Total amount (inclusive GST) of the AWB')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price (exclusive of GST) of the order')

    address_line = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    pincode = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    sms_contact = models.CharField(max_length=500)
