from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from flashdeal.apis.user_apis import UserRegisterAPI
from flashdeal.apis.vendor_apis import VendorRetrieveUpdateCreateAPI
from flashdeal.views.catalog_views import CatalogListView, CatalogCreateView, CatalogSubmitView
from flashdeal.views.flashdeal_views import FlashDealCreateView, FlashDealListView
from flashdeal.views.product_views import ProductListView, ProductDetailView, ProductCreateView

app_name = 'flashdeal'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),

    path('flashdeal/create/', FlashDealCreateView.as_view(), name='flashdeal_create'),
    path('flashdeal/', FlashDealListView.as_view(), name='flashdeal_list'),

    path('catalogs/', CatalogListView.as_view(), name='catalog_list'),
    path('catalogs/create/', CatalogCreateView.as_view(), name='catalog_create'),
    path('catalogs/<int:pk>/submit/', CatalogSubmitView.as_view(), name='catalog_submit'),

    path('api/vendor/', VendorRetrieveUpdateCreateAPI.as_view(), name='post_vendor'),
    path('api/vendor/<int:pk>/', VendorRetrieveUpdateCreateAPI.as_view(), name='get_vendor'),

    path('api/token/', obtain_jwt_token, name='token_create'),
    path('api/token/refresh/', refresh_jwt_token, name='token_refresh'),

    path('api/user/register/', UserRegisterAPI.as_view(), name='user_register'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
