from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from flashdeal.test.base_request_test import BaseTest


class UserTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.phone_number = self.f.phone_number()
        self.data = {
            'phone': self.phone_number,
        }

    def test_register_new_user(self):
        url = reverse('flashdeal:user_register')
        resp = self.client.post(url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_get_user_token(self):
        self.test_register_new_user()
        url = reverse('flashdeal:token_create')
        resp = self.client.post(url, data={
            'phone': self.data['phone'],
            'otp': '2221'
        })
        data = resp.json()
        self.assertEqual(User.objects.get(username=self.phone_number).is_active, True)
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertNotEqual(data.get('token'), None)

    def test_get_user_token_with_wrong_otp(self):
        self.test_register_new_user()
        url = reverse('flashdeal:token_create')
        resp = self.client.post(url, data={
            'phone': self.data['phone'],
            'otp': '2222'
        })
        self.assertEqual(User.objects.get(username=self.phone_number).is_active, False)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.data, None)

    def test_refresh_token_of_user(self):
        self.test_register_new_user()
        resp = self.client.post(reverse('flashdeal:token_create'), data={
            'phone': self.data['phone'],
            'otp': '2221'
        })
        token = resp.json()['token']
        now_timestamp = timegm((datetime.utcnow()).utctimetuple())
        resp_refresh = self.client.post(reverse('flashdeal:token_refresh'), data={
            'token': token,
            'orig_iat': now_timestamp
        })
        data = resp_refresh.json()
        print(data)
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertNotEqual(data.get('token'), None)
