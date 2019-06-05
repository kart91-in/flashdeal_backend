from django.db import models
from django.utils.timezone import now

from core.models import BaseModel


class FlashDeal(BaseModel):

    name = models.CharField(max_length=500, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    catalog = models.ForeignKey('flashdeal.Catalog', on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.start_time:
            self.start_time = now()
        super().save(force_insert, force_update, using, update_fields)