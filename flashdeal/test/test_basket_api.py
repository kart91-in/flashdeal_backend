from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from flashdeal.fixtures import gen_products
from flashdeal.test.base_request_test import BaseTest


class BasketTest(BaseTest):
    fixtures = ['colors.json', 'sizes.json']

    def setUp(self):
        super().setUp()
        self.login_user()
        self.products = gen_products(3)
        self.products = gen_products(3)

    def test_add_a_product_to_basket(self):


        url = reverse('flashdeal:add_basket_product')
        resp = self.client.put(url, data={
            'variant_id': self.products[0].variants.first().id
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotEqual(resp.json().get('product_variants'), [])

    def test_remove_a_product_to_basket(self):
        url = reverse('flashdeal:add_basket_product')
        self.client.put(url, data={
            'variant_id': self.products[0].variants.first().id
        })
        self.assertEqual(self.user.basket.product_variants.first().id , self.products[0].id)

        url = reverse('flashdeal:remove_basket_product')
        resp = self.client.put(url, data={
            'variant_id': self.products[0].variants.first().id
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json().get('product_variants'), [])

