from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel


class UserProfile(BaseModel):

    user = models.OneToOneField(User, primary_key=True, on_delete=models.PROTECT, related_name='profile')
    phone = models.CharField(max_length=500, unique=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    is_validated = models.BooleanField(default=False)
