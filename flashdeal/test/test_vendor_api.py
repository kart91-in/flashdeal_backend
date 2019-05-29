from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from flashdeal.models import Vendor
from flashdeal.test.base_request_test import BaseTest


class VendorTest(BaseTest):

    def setUp(self):
        super().setUp()
        vendor_user = User.objects.create_user('username', 'email@gmail.com', 'password')
        self.data = {
            'user_id': vendor_user.id,
            'name': 'name1',
            'email': 'company@gmail.com',
            'gstin_number': 1123123,
            'phone': 1123123,
            'status': 1,
        }

    def test_create_valid_vendor_item(self):
        url = reverse('flashdeal:post_vendor')
        resp = self.client.post(url, data=self.data)

        self.assertEqual(self.data['user_id'], resp.json()['user_id'])
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_get_existed_item(self):
        vendor = Vendor.objects.create(**self.data)
        url = reverse('flashdeal:get_vendor', kwargs={'pk': vendor.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(vendor.pk, resp.json()['user_id'])

    def test_get_not_existed_item(self):
        url = reverse('flashdeal:get_vendor', kwargs={'pk': 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        new_name = 'A new name'
        vendor = Vendor.objects.create(**self.data)
        url = reverse('flashdeal:get_vendor', kwargs={'pk': vendor.pk})
        resp = self.client.put(url, {**self.data, 'name': new_name})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['name'], new_name)
