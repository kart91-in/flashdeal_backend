from django.urls import reverse
from django.views import generic

from flashdeal.forms import CreateProductForm
from flashdeal.models import Product
from flashdeal.views.mixins import LeftBarMixin


class ProductDetailView(LeftBarMixin, generic.DetailView):
    model = Product
    template_name = 'dashboard/product_detail.html'


class ProductListView(LeftBarMixin, generic.ListView):

    template_name = 'dashboard/product_list.html'
    ordering = ('-created_at', )

    def get_queryset(self):
        current_vendor = self.request.user.vendor
        return Product.objects.filter(vendor=current_vendor)


class ProductCreateView(LeftBarMixin, generic.CreateView):

    template_name = 'dashboard/product_create.html'
    form_class = CreateProductForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('flashdeal:product_list')
