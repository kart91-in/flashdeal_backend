from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from flashdeal.fixtures import gen_products
from flashdeal.models import Basket
from flashdeal.models.product_models import ProductVariant
from flashdeal.test.base_request_test import BaseTest


class OrderTest(BaseTest):

    fixtures = ['colors.json', 'sizes.json']

    def setUp(self):
        super().setUp()
        self.login_user()
        self.products = gen_products(3)
        self.buy_product = ProductVariant.objects.all()[:2]
        Basket.objects.create(user=self.user)
        self.user.basket.product_variant.set(self.buy_product)
        self.order_data = {
            'name': self.f.name(),
            'address': self.f.address(),
            'phone': self.f.phone_number(),
            'city': self.f.city(),
            'pin_code': self.f.postcode(),
        }
        self.payment_data = {
            'transaction_id': self.f.random_number(6, True),
            'gateway_order_id': self.f.random_number(10, True),
            'gateway': self.f.company(),
            'meta': {
                'ip': self.f.ipv4(),
            },

        }

    def test_create_an_order_from_basket(self):
        url = reverse('flashdeal:order')
        resp = self.client.post(url, data=self.order_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.json()['status'], 'Just created')
        self.assertEqual(len(resp.json()['products']), 3)

    def test_make_a_payment_to_an_order(self):
        # Make an order first
        url = reverse('flashdeal:order')
        order_resp = self.client.post(url, data=self.order_data)

        # Do dummy Payment
        url = reverse('flashdeal:payment')
        self.payment_data.update({
            'amount' : order_resp.json()['total_price'],
            'order' : order_resp.json()['id'],
        })
        resp = self.client.post(url, data=self.payment_data, format='json')
        print(resp.json())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
