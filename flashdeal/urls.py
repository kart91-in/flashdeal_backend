from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from flashdeal.apis.basket_apis import BasketRetrieveUpdateDeleteAPI
from flashdeal.apis.catalog_apis import CatalogListCreateAPI
from flashdeal.apis.order_apis import OrderRetrieveUpdateDeleteAPI
from flashdeal.apis.payment_apis import PaymentRetrieveCreateDeleteAPI
from flashdeal.apis.product_apis import ProductListCreateAPI, \
    ProductDestroyUpdateAPI, ProductColorListAPI, ProductSizeListAPI
from flashdeal.apis.user_apis import UserRegisterAPI, UserTokenAPI, UserResendOtpAPI
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

    # path('catalogs/', CatalogListView.as_view(), name='catalog_list'),
    path('catalogs/create/', CatalogCreateView.as_view(), name='catalog_create'),
    path('catalogs/<int:pk>/submit/', CatalogSubmitView.as_view(), name='catalog_submit'),

    path('api/catalogs/', CatalogListCreateAPI.as_view(), name='catalog'),

    path('api/product/size/', ProductSizeListAPI.as_view(), name='product_size'),
    path('api/product/color/', ProductColorListAPI.as_view(), name='product_color'),

    path('api/product/', ProductListCreateAPI.as_view(), name='product'),
    path('api/product/<int:pk>/', ProductDestroyUpdateAPI.as_view(), name='product_object'),

    path('api/vendor/', VendorRetrieveUpdateCreateAPI.as_view(), name='post_vendor'),
    path('api/vendor/<int:pk>/', VendorRetrieveUpdateCreateAPI.as_view(), name='get_vendor'),

    path('api/basket/products/add/', BasketRetrieveUpdateDeleteAPI.as_view(),
         name='add_basket_product'),
    path('api/basket/', BasketRetrieveUpdateDeleteAPI.as_view(),
         name='basket_product'),
    path('api/basket/products/remove/', BasketRetrieveUpdateDeleteAPI.as_view(remove_product=True),
         name='remove_basket_product'),

    path('api/order/', OrderRetrieveUpdateDeleteAPI.as_view(), name='order'),
    path('api/payment/', PaymentRetrieveCreateDeleteAPI.as_view(), name='payment'),

    path('api/token/create/', obtain_jwt_token, name='token_create'),
    path('api/token/refresh/', refresh_jwt_token, name='token_refresh'),
    path('api/token/', UserTokenAPI.as_view(), name='token_create'),
    path('api/token/resend_otp/', UserResendOtpAPI.as_view(), name='token_otp_resend'),

    path('api/user/register/', UserRegisterAPI.as_view(), name='user_register'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
