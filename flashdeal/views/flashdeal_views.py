from django.urls import reverse
from django.views import generic

from flashdeal.forms import CreateFlashDealForm
from flashdeal.models import FlashDeal
from flashdeal.views.mixins import LeftBarMixin


class FlashDealListView(LeftBarMixin, generic.ListView):

    template_name = 'dashboard/flashdeal_list.html'

    def get_queryset(self):
        current_vendor = self.request.user.vendor
        return FlashDeal.objects.filter(catalog__vendor=current_vendor)


class FlashDealCreateView(LeftBarMixin, generic.CreateView):

    template_name = 'dashboard/flashdeal_create.html'
    form_class = CreateFlashDealForm

    def get_success_url(self):
        return reverse('flashdeal:flashdeal_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'catalog_id': self.request.GET.get('catalog_id'),
        })
        return kwargs

