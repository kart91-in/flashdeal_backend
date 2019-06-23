import json
from django.urls import reverse
from rest_framework import status

from flashdeal.fixtures import gen_products
from flashdeal.models import Basket, Order
from flashdeal.models.order_models import DeliveryInfo, ReturnOrder
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

    def test_verify_an_order(self):
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
            'rto_city': 'city 1',
            'rto_contact_no': self.f.random_number(10, True),
            'rto_address': self.f.address(),
            'rto_pincode': 110003,
        }
        order_id = resp.json()['order_id']
        order = Order.objects.get(id=order_id)
        resp = self.client.post(reverse('flashdeal:order_delivery_info', kwargs={'pk': order_id}),
                                data=delivery_info, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order.status, Order.STATUS_PAYMENT)

    def test_return_an_order(self):
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
            'pickup_address_pincode': 400033,
            'rto_name': self.f.name(),
            'rto_state': 'bihar',
            'rto_city': 'city 1',
            'rto_contact_no': self.f.random_number(10, True),
            'rto_address': self.f.address(),
            'rto_pincode': 110003,
        }
        print(json.dumps(delivery_info))
        order_id = resp.json()['order_id']
        order = Order.objects.get(id=order_id)
        resp = self.client.post(reverse('flashdeal:order_delivery_info', kwargs={'pk': order_id}),
                                data=delivery_info, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order.status, Order.STATUS_PAYMENT)

        return_data = {
            'warehouse_name': self.f.company(),
            'warehouse_address': self.f.address(),
            'address_line': self.f.address(),
            'city': self.f.city(),
            'phone_number': '91312858236',
            'sms_contact': '91312858236',
            'name': self.f.company(),
            'country': 'India',
            'destination_pincode': 400033,
            'pincode': 400033,
        }

        resp = self.client.post(
            reverse('flashdeal:order_return', kwargs={'pk': order_id}),
            data=return_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        return_order_id = resp.json()['id']
        resp = self.client.post(
            reverse('flashdeal:order_return_send', kwargs={'pk': return_order_id}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotEqual(ReturnOrder.objects.get(pk=return_order_id).status, ReturnOrder.STATUS_NOT_SEND)

