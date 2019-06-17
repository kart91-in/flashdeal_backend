from rest_framework.generics import RetrieveUpdateAPIView, mixins
from rest_framework.permissions import AllowAny
from flashdeal.models.vendor_models import Vendor
from flashdeal.serializers.vendor_serializers import VendorSerializer


class VendorRetrieveUpdateCreateAPI(mixins.CreateModelMixin, RetrieveUpdateAPIView):

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

