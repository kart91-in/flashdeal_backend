import json
from django.urls import reverse
from rest_framework import status

from flashdeal.fixtures import gen_products
from flashdeal.models import Basket, Order
from flashdeal.models.order_models import DeliveryInfo
from flashdeal.models.product_models import ProductVariant
from flashdeal.test.base_request_test import BaseTest


class OrderTest(BaseTest):

    fixtures = ['colors.json', 'sizes.json', 'awb.json']

    def setUp(self):
        super().setUp()
        self.login_user()
        self.products = gen_products(3)
        self.buy_product = ProductVariant.objects.all()[:2]
        Basket.objects.create(user=self.user)
        self.user.basket.add_product_variant(self.buy_product[1])
        self.user.basket.add_product_variant(self.buy_product[1])
        self.user.basket.add_product_variant(self.buy_product[0])
        self.order_data = {
            'customer_name': self.f.name(),
            'customer_address': self.f.address(),
            'customer_phone': self.f.random_number(10, True),
            'alternate_customer_contact': self.f.random_number(10, True),
            'address_type': 'home',
            'c_city': self.f.city(),
            'c_state': 'bihar',
            'pin_code': 110003,
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
        self.assertEqual(len(resp.json()['purchases']), 2)

    def test_make_a_payment_to_an_order(self):
        # Make an order first
        url = reverse('flashdeal:order')
        order_resp = self.client.post(url, data=self.order_data)

        # Do dummy Payment
        url = reverse('flashdeal:payment_list')
        self.payment_data.update({
            'amount' : order_resp.json()['total_price'],
            'order' : order_resp.json()['id'],
        })
        resp = self.client.post(url, data=self.payment_data, format='json')
        order = Order.objects.get(id=order_resp.json()['id'])
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order.status, Order.STATUS_PAYMENT)

    def test_verify_a_order(self):
        url = reverse('flashdeal:order')
        order_resp = self.client.post(url, data=self.order_data)

        # Do dummy Payment
        url = reverse('flashdeal:payment_list')
        self.payment_data.update({
            'amount': order_resp.json()['total_price'],
            'order': order_resp.json()['id'],
        })
        resp = self.client.post(url, data=self.payment_data, format='json')

        delivery_info = {
            'actual_weight': 10,
            'volumetric_weight': 10,
            'pincode': 110005,
            'pickup_address': self.f.address(),
            'pickup_address_pincode': 110026,
            'rto_name': self.f.name(),
            'rto_state': 'bihar',
            'rto_contact_no': self.f.random_number(10, True),
            'rto_address': self.f.address(),
            'rto_pincode': 110003,
        }
        order_id = resp.json()['order_id']
        order = Order.objects.get(id=order_id)
        delivery_info = DeliveryInfo.objects.create(order=order, **delivery_info)
        self.assertEqual(order.status, Order.STATUS_VERIFIED)
