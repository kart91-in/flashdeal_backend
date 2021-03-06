from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from core.models import BaseModel, BaseApprovalLogModel
from flashdeal.contances import STATE_LIST


class Vendor(BaseModel):

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

    user = models.OneToOneField(User, primary_key=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=500)
    email = models.EmailField(blank=True, null=True)
    gstin_number = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    state = models.CharField(max_length=500, choices=STATE_LIST)
    phone = models.CharField(max_length=500, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=STATUS_NOT_VERIFIED, choices=STATUS)

    def approve(self, by_user):
        if self.status != self.STATUS_NOT_VERIFIED:
            raise ValidationError('This Vendor is not in state to approve')
        self.status = self.STATUS_VERIFIED
        self.save()
        self.logs.create(user=by_user, type=VendorApprovalLog.TYPE_APPROVE)

    def reject(self, by_user, note):
        if self.status != self.STATUS_NOT_VERIFIED:
            raise ValidationError('This Vendor is not in state to reject')
        self.status = self.STATUS_REJECTED
        self.save()
        self.logs.create(user=by_user, note=note, type=VendorApprovalLog.TYPE_REJECT)

    def disable(self, by_user, note):
        if self.status == self.STATUS_DISABLE:
            raise ValidationError('This Vendor is not in state to disable')
        self.status = self.STATUS_DISABLE
        self.save()
        self.logs.create(user=by_user, note=note, type=VendorApprovalLog.TYPE_DISABLE)


class VendorApprovalLog(BaseApprovalLogModel):

    TYPE_DISABLE = 2

    TYPE = BaseApprovalLogModel.TYPE + (
        (TYPE_DISABLE, 'Disable'),
    )

    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, related_name='logs',
                               related_query_name='log')

