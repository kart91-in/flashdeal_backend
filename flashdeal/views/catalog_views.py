from django.urls import reverse
from django.views import generic

from flashdeal.forms import CreateCatalogForm
from flashdeal.models import Catalog
from flashdeal.views.mixins import LeftBarMixin


class CatalogListView(LeftBarMixin, generic.ListView):
    template_name = 'dashboard/catalog_list.html'
    ordering = ('-created_at', )

    def get_queryset(self):
        current_vendor = self.request.user.vendor
        return Catalog.objects.filter(vendor=current_vendor)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**{
            **kwargs,
            'message': self.request.session.pop('message', None),
            'error': self.request.session.pop('error', None)
        })


class CatalogCreateView(LeftBarMixin, generic.CreateView):
    template_name = 'dashboard/catalog_create.html'
    form_class = CreateCatalogForm

    def get_success_url(self):
        return reverse('flashdeal:catalog_list')

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'user': self.request.user,
        }


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

