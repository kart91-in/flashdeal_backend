from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class BaseTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        self.client.force_authenticate(self.user)

