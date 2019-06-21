from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, mixins, \
    UpdateAPIView, get_object_or_404, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from flashdeal.models.vendor_models import Vendor
from flashdeal.serializers.vendor_serializers import VendorSerializer


class VendorListCreateAPI(ListCreateAPIView):
    serializer_class = VendorSerializer
    queryset = Vendor.objects


class VendorRetrieveUpdateCreateAPI(RetrieveUpdateAPIView):

    serializer_class = VendorSerializer
    permission_classes = (IsAdminUser, )

    def get_object(self):
        return get_object_or_404(Vendor, pk=self.kwargs.get('pk'))


class ApproveVendorAPI(UpdateAPIView):

    permission_classes = (IsAdminUser, )

    def put(self, request, *args, **kwargs):
        obj = get_object_or_404(Vendor, pk=self.kwargs.get('pk'))
        obj.approve(request.user)
        return Response(status=status.HTTP_200_OK)


class RejectVendorAPI(UpdateAPIView):

    permission_classes = (IsAdminUser, )

    def put(self, request, *args, **kwargs):
        obj = get_object_or_404(Vendor, pk=self.kwargs.get('pk'))
        obj.reject(request.user, request.data.get('note'))
        return Response(status=status.HTTP_200_OK)