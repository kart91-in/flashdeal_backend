from django.urls import reverse
from django.views import generic

from flashdeal.forms import CreateProductForm, CreateCatalogForm
from flashdeal.models import Product, Catalog


class LeftBarMixin(object):

    def get_leftbar_apps(self):
        return [
            {
                'text': 'Your Products',
                'url': '#',
                'icon': 'home',
                'sub_item': [
                    {
                        'text': 'Product list',
                        'url': reverse('flashdeal:product_list'),
                    },
                    {
                        'text': 'Add a Product',
                        'url': reverse('flashdeal:product_create'),
                    },
                    {
                        'text': 'Catalog list',
                        'url': reverse('flashdeal:catalog_list'),
                    },
                    {
                        'text': 'Add a Catalog',
                        'url': reverse('flashdeal:catalog_create'),
                    }
                ]
            },
        ]

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['app_list'] = self.get_leftbar_apps()
        return super().get_context_data(**kwargs)


class ProductDetailView(LeftBarMixin, generic.DetailView):
    model = Product
    template_name = 'dashboard/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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

    def form_valid(self, form):
        form._image_list = self.request.FILES.getlist('image_list')
        return super().form_valid(form)


class CatalogListView(LeftBarMixin, generic.ListView):
    template_name = 'dashboard/catalog_list.html'
    ordering = ('-created_at', )

    def get_queryset(self):
        current_vendor = self.request.user.vendor
        return Catalog.objects.filter(vendor=current_vendor)

    def get_context_data(self, **kwargs):
        kwargs['message'] = self.request.session.pop('message', None)
        kwargs['error'] = self.request.session.pop('error', None)
        return super().get_context_data(**kwargs)


class CatalogCreateView(LeftBarMixin, generic.CreateView):
    template_name = 'dashboard/catalog_create.html'
    form_class = CreateCatalogForm

    def get_success_url(self):
        return reverse('flashdeal:catalog_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['_image_list'] = self.request.FILES.getlist('image_list')
        return kwargs


class CatalogSubmitView(generic.RedirectView):
    pattern_name = 'flashdeal:catalog_list'
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        catalog_pk = kwargs.pop('pk')
        try:
            Catalog.objects.get(pk=catalog_pk).submit_for_approval()
            self.request.session['message'] = f'Catelog id #{catalog_pk} is submitted for approval'
        except Exception as e:
            self.request.session['error'] = e.message
        return super().get_redirect_url(*args, **kwargs)
