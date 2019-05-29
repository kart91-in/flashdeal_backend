from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from flashdeal.apis import VendorRetrieveUpdateCreateAPI

app_name = 'flashdeal'

urlpatterns = [
    path('api/vendor/', VendorRetrieveUpdateCreateAPI.as_view(), name='post_vendor'),
    path('api/vendor/<int:pk>/', VendorRetrieveUpdateCreateAPI.as_view(), name='get_vendor'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
