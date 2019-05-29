from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return getattr(self, 'name', super().__str__())


class BaseApprovalLogModel(BaseModel):

    TYPE_APPROVE = 0
    TYPE_REJECT = 1

    TYPE = (
        (TYPE_APPROVE, 'Approve'),
        (TYPE_REJECT, 'Reject'),
    )

    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.PositiveSmallIntegerField(default=TYPE[0][0], choices=TYPE)
    note = models.CharField(max_length=500, null=True, blank=True)


