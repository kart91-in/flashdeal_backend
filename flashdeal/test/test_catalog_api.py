import json
from random import randrange
from django.urls import reverse
from rest_framework import status

from flashdeal.fixtures import add_vendor_profile, gen_products
from flashdeal.models.product_models import ProductColor, ProductSize, Product
from flashdeal.test.base_request_test import BaseTest


class CatalogTest(BaseTest):
    fixtures = ['colors.json', 'sizes.json']

    def setUp(self):
        super().setUp()
        self.login_user()
        add_vendor_profile(self.user)
        self.products = gen_products(3)

        product_ids = list(Product.objects.all()[:2].values_list('pk', flat=True))
        self.data = {
            'name': self.f.job(),
            'description': self.f.text(),
            'product_ids': product_ids
        }
        self.data_update = {
            'name': self.f.job(),
            'description': self.f.text(),
            'product_ids': product_ids[:-1]
        }


    def test_create_catalog_with_products(self):
        url = reverse('flashdeal:catalog')
        resp = self.client.post(url, data=self.data, format='json')
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(data.get('products')), 2)

    def test_update_catalog_with_products(self):
        url = reverse('flashdeal:catalog')
        resp = self.client.post(url, data=self.data, format='json')
        data = resp.json()
        self.assertEqual(len(data.get('products')), 2)

        resp = self.client.put(reverse('flashdeal:catalog_object', kwargs={'pk': data.get('id')}),
                                data=self.data_update, format='json')
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data.get('products')), 1)
        self.assertEqual(data.get('name'), self.data_update.get('name'))