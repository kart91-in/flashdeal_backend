from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from flashdeal.apis import VendorRetrieveUpdateCreateAPI
from flashdeal.views import ProductListView, ProductCreateView, CatalogCreateView

app_name = 'flashdeal'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create', ProductCreateView.as_view(), name='product_create'),
    path('catalogs/create', CatalogCreateView.as_view(), name='catalog_create'),
    path('api/vendor/', VendorRetrieveUpdateCreateAPI.as_view(), name='post_vendor'),
    path('api/vendor/<int:pk>/', VendorRetrieveUpdateCreateAPI.as_view(), name='get_vendor'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
