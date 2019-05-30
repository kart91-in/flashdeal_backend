from django.contrib.auth.models import User
from faker import Faker

from flashdeal.models import Vendor


def gen_users(number=1, **kwargs):
    fa = Faker()
    for i in range(number):
        yield User.objects.create_user(
            username=fa.name(),
            email=fa.email(),
            password='pass',
        )

def gen_vendors(number=1, **kwargs):
    fa = Faker()
    for user in gen_users(number):
        yield Vendor.objects.create(
            user=user,
            name=fa.company(),
            email=fa.email(),
            gstin_number=fa.random_number(6),
            address=fa.address()
        )
