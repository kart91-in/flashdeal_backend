from django.core.exceptions import ValidationError
from django.db import models
from core.models import BaseModel, BaseApprovalLogModel
from flashdeal.models import Vendor, Product


class Catalog(BaseModel):

    STATUS_NOT_VERIFIED = 0
    STATUS_VERIFIED = 1
    STATUS_REJECTED = 2
    STATUS_DISABLE = 3

    STATUS = (
        (STATUS_NOT_VERIFIED, 'Not Verified'),
        (STATUS_VERIFIED, 'Verified'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_DISABLE, 'Disabled'),
    )

    name = models.CharField(max_length=500)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='catalogs',
                               related_query_name='catalog')
    status = models.PositiveSmallIntegerField(default=STATUS[0][0], choices=STATUS)
    products = models.ManyToManyField(Product, blank=True, related_name='catalogs', related_query_name='catalog')

    def approve(self, by_user):
        if self.status != self.STATUS_NOT_VERIFIED:
            raise ValidationError('This Catalog is not in state to approve')
        self.status = self.STATUS_VERIFIED
        self.save()
        self.logs.create(user=by_user, type=CatalogApprovalLog.TYPE_APPROVE)

    def reject(self, by_user, note):
        if self.status != self.STATUS_NOT_VERIFIED:
            raise ValidationError('This Catalog is not in state to reject')
        self.status = self.STATUS_REJECTED
        self.save()
        self.logs.create(user=by_user, note=note, type=CatalogApprovalLog.TYPE_REJECT)


class CatalogApprovalLog(BaseApprovalLogModel):

    vendor = models.ForeignKey('Catalog', on_delete=models.PROTECT,
                               related_name='logs',
                               related_query_name='log')

