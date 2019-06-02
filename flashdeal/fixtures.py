from random import random, uniform

from django.contrib.auth.models import User
from faker import Faker

from flashdeal.models import Vendor, Product


def gen_users(number=1, **kwargs):
    fa = Faker()
    return [User.objects.create_user(
        username=fa.name()[0],
        email=fa.email()[0],
        password='pass',
    ) for i in range(number)]

def gen_vendors(number=1, **kwargs):
    fa = Faker()
    user = gen_users(number)[0]
    return [Vendor.objects.create(
        user=user,
        name=fa.company()[0],
        email=fa.email()[0],
        gstin_number=fa.random_number(6),
        address=fa.address()
    ) for i in range(number)]

def gen_product_for_vendors(vendor_id=None, number=1, **kwargs):
    fa = Faker()
    if not vendor_id:
        vendor_id = gen_vendors(1)[0].id
    return [Product.objects.create(
        vendor_id=vendor_id,
        name=fa.sentences()[0],
        upper_price=100.59,
        sale_price=uniform(10.5, 100.5)
    ) for i in range(number)]

