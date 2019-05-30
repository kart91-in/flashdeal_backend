from rest_framework.generics import mixins, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from flashdeal.models.vendor_models import Vendor
from flashdeal.serializers import VendorSerializer


class VendorRetrieveUpdateCreateAPI(mixins.CreateModelMixin, RetrieveUpdateAPIView):

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)