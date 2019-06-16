from django.core.exceptions import ValidationError
from django.db import models
from core.models import BaseModel, BaseApprovalLogModel


class Catalog(BaseModel):

    STATUS_NOT_VERIFIED = 0
    STATUS_VERIFIED = 1
    STATUS_REJECTED = 2
    STATUS_DISABLE = 3
    STATUS_SUBMITTED = 3

    STATUS = (
        (STATUS_NOT_VERIFIED, 'Not Verified'),
        (STATUS_VERIFIED, 'Verified'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_DISABLE, 'Disabled'),
        (STATUS_SUBMITTED, 'Submitted for approval'),
    )

    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey('flashdeal.Vendor', on_delete=models.PROTECT, related_name='catalogs',
                               related_query_name='catalog')
    status = models.PositiveSmallIntegerField(default=STATUS_NOT_VERIFIED, choices=STATUS)
    products = models.ManyToManyField('flashdeal.Product', blank=True, related_name='catalogs', related_query_name='catalog')

    def is_verified(self):
        return self.status == self.STATUS_VERIFIED

    def is_submitted(self):
        self.get_status_display()
        return self.status == self.STATUS_SUBMITTED

    def submit_for_approval(self):
        if self.status not in [self.STATUS_REJECTED, self.STATUS_NOT_VERIFIED]:
            raise ValidationError('This Catalog is not in state to submit')
        self.status = self.STATUS_SUBMITTED
        self.save()
        self.logs.create(user=self.vendor.user, type=CatalogApprovalLog.TYPE_SUBMIT)

    def approve(self, by_user):
        if not self.is_submitted():
            raise ValidationError('This Catalog is not in state to approve')
        self.status = self.STATUS_VERIFIED
        self.save()
        self.logs.create(user=by_user, type=CatalogApprovalLog.TYPE_APPROVE)

    def reject(self, by_user, note):
        if not self.is_submitted():
            raise ValidationError('This Catalog is not in state to reject')
        self.status = self.STATUS_REJECTED
        self.save()
        self.logs.create(user=by_user, note=note, type=CatalogApprovalLog.TYPE_REJECT)


class CatalogApprovalLog(BaseApprovalLogModel):

    TYPE_SUBMIT = 2

    TYPE = BaseApprovalLogModel.TYPE + (
        (TYPE_SUBMIT, 'Submit for approval')
    )

    vendor = models.ForeignKey('Catalog', on_delete=models.PROTECT,
                               related_name='logs',
                               related_query_name='log')

