import json
from random import randrange
from unittest import mock
from django.core.files import File

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from flashdeal.fixtures import add_vendor_profile
from flashdeal.models import Vendor
from flashdeal.models.product_models import ProductColor, ProductSize, Product
from flashdeal.test.base_request_test import BaseTest


class CatalogTest(BaseTest):
    fixtures = ['colors.json', 'sizes.json']

    def setUp(self):
        super().setUp()
        self.login_user()
        add_vendor_profile(self.user)
        colors = list(ProductColor.objects.all()[:2].values_list('pk', flat=True))
        sizes = list(ProductSize.objects.all()[:2].values_list('pk', flat=True))
        self.data = {
            'name': self.f.job(),
            'description': self.f.text(),
            'sale_price': randrange(10, 20),
            'upper_price': randrange(20, 30),
            'image_files': [
                self._create_image(),
                self._create_image(),
            ],
            'variants': json.dumps([
                {
                    'color': colors[0],
                    'size': sizes[0],
                    'sale_price': randrange(10, 20),
                },
                {
                    'color': colors[1],
                    'size': sizes[1],
                    'stock': 5
                }
            ])
        }
        self.data_update = {
            'name': self.f.job(),
            'description': self.f.text(),
            'sale_price': randrange(10, 20),
            'upper_price': randrange(20, 30),
        }


    def test_create_product(self):
        url = reverse('flashdeal:product')

        resp = self.client.post(url, data=self.data, format='multipart')
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(data.get('id'))
        self.assertIsNotNone(data.get('product_variants'))
        self.assertIsNotNone(data.get('images'))

    def test_get_list_product(self):
        url = reverse('flashdeal:product')
        self.client.post(url, data=self.data, format='multipart')

        resp = self.client.get(url)
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)

    def test_delete_product(self):
        url = reverse('flashdeal:product')
        resp = self.client.post(url, data=self.data, format='multipart')
        data = resp.json()
        obj_pk = data.get('id')

        url = reverse('flashdeal:product_object', kwargs={'pk': obj_pk})
        resp = self.client.delete(url)

        product = Product.objects.filter(pk=obj_pk).exists()
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(product, False)

    def test_update_product(self):
        url = reverse('flashdeal:product')
        resp = self.client.post(url, data=self.data, format='multipart')
        data = resp.json()
        obj_pk = data.get('id')

        url = reverse('flashdeal:product_object', kwargs={'pk': obj_pk})
        resp = self.client.patch(url, data=self.data_update, format='json')
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('id'), obj_pk)
        self.assertEqual(data.get('name'), self.data_update.get('name'))
