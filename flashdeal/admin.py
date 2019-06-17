from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.utils.html import format_html
from flashdeal.forms import AddLogNoteForm
from flashdeal.models import Product, Image, Catalog, Video, FlashDeal, Order
from flashdeal.models.order_models import DeliveryInfo, AWBNumber
from flashdeal.models.vendor_models import Vendor, VendorApprovalLog


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'status', 'email', 'vendor_actions', 'created_at')
    fields = (
        'user', 'status', 'name', 'email',
        'gstin_number', 'address', 'phone',
    )
    search_fields = ('name__icontains', 'email__icontains')
    list_filter = ('status', )

    def vendor_actions(self, obj):
        if obj.status != Vendor.STATUS_NOT_VERIFIED:
            return '--'
        approve = reverse('admin:approve-vendor', args=[obj.pk])
        reject = reverse('admin:reject-vendor', args=[obj.pk])

        return format_html(f'<a onclick="return confirm(\'Do you really want to approve this vendor?\');"  class="button" href="{approve}">Approve</a> '
                           f'<a onclick="return confirm(\'Do you really want to reject this vendor?\');"  class="button danger" href="{reject}">Reject</a> ')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/approve/',
                self.admin_site.admin_view(self.approve_vendor),
                name='approve-vendor',
            ),
            path(
                '<path:object_id>/reject/',
                self.admin_site.admin_view(self.reject_vendor),
                name='reject-vendor',
            ),
        ]
        return custom_urls + urls

    def to_change_list(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect(reverse('admin:%s_%s_changelist' % info))

    def approve_vendor(self, request, object_id, *args, **kwargs):
        try:
            vendor = self.get_object(request, object_id)
            vendor.approve(by_user=request.user)
            self.message_user(request, 'Approved Vendor', messages.SUCCESS)
        except ValidationError as e:
            self.message_user(request, e.message, messages.ERROR)
        return self.to_change_list()

    def reject_vendor(self, request, object_id, *args, **kwargs):
        context = self.admin_site.each_context(request)
        if request.method != 'POST':
            context['form'] = AddLogNoteForm()
        else:
            form = AddLogNoteForm(request.POST)
            if form.is_valid():
                try:
                    note = form.cleaned_data['note']
                    vendor = self.get_object(request, object_id)
                    vendor.reject(by_user=request.user, note=note)
                    self.message_user(request, 'Rejected Vendor', messages.SUCCESS)
                except ValidationError as e:
                    self.message_user(request, e.message, messages.ERROR)
            else:
                self.message_user(request, form.errors[0], messages.ERROR)
            return self.to_change_list()
        return TemplateResponse(request, 'admin/flashdeal/form_submit.html', context)


@admin.register(VendorApprovalLog)
class VendorApprovalLogAdmin(admin.ModelAdmin):

    list_display = ('vendor', 'type', 'by_user', 'note', 'created_at')

    def by_user(self, obj):
        return obj.user


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('vendor', 'name', 'image_url', 'sale_price', 'upper_price', 'created_at', )

    def image_url(self, obj):
        image_url = obj.image_url()
        if not image_url: return '---'
        return format_html(f'<img width=100 src={image_url}/>')


@admin.register(DeliveryInfo)
class DeliveryAdmin(admin.ModelAdmin):

    list_display = ('order', 'awb_number', 'created_at', )
    list_filter = ('status', )


@admin.register(AWBNumber)
class AWBNumberAdmin(admin.ModelAdmin):
    list_display = ('value', 'is_used', )
    list_filter = ('is_used', )
    ordering = ('is_used', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery_info', 'status', 'customer_name', 'created_at', 'order_actions')
    list_filter = ('status', )

    def order_actions(self, obj):
        create_delivery = reverse('admin:flashdeal_delivery_add') + f'?order={obj.pk}'
        return format_html(f'<a target="_blank" class="button" href="{create_delivery}">Deliver</a>')


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):

    list_display = ('name', 'vendor', 'status', 'created_at', 'product_count', 'catalog_actions')
    list_filter = ('status', )
    # inlines = (CatalogImageInline, CatalogVideoInline)

    def product_count(self, obj):
        return f'{obj.products.all().count()} product(s)'

    def catalog_actions(self, obj):
        if obj.status == Catalog.STATUS_VERIFIED:
            create_flashdeal = reverse('admin:flashdeal_flashdeal_add') + f'?catalog={obj.pk}'
            return format_html(f'<a target="_blank" class="button" href="{create_flashdeal}">FlashDeal</a>')

        if obj.status == Catalog.STATUS_SUBMITTED:
            approve = reverse('admin:approve-catalog', args=[obj.pk])
            reject = reverse('admin:reject-catalog', args=[obj.pk])
            return format_html(f'<a onclick="return confirm(\'Do you really want to approve this catalog?\');" class="button" href="{approve}">Approve</a> '
                               f'<a onclick="return confirm(\'Do you really want to reject this catalog?\');" class="button danger" href="{reject}">Reject</a> ')
        return '--'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/approve/',
                self.admin_site.admin_view(self.approve_catalog),
                name='approve-catalog',
            ),
            path(
                '<path:object_id>/reject/',
                self.admin_site.admin_view(self.reject_catalog),
                name='reject-catalog',
            ),
        ]
        return custom_urls + urls

    def to_change_list(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect(reverse('admin:%s_%s_changelist' % info))

    def approve_catalog(self, request, object_id, *args, **kwargs):
        try:
            vendor = self.get_object(request, object_id)
            vendor.approve(by_user=request.user)
            self.message_user(request, 'Approved Catalog', messages.SUCCESS)
        except ValidationError as e:
            self.message_user(request, e.message, messages.ERROR)
        return self.to_change_list()

    def reject_catalog(self, request, object_id, *args, **kwargs):
        context = self.admin_site.each_context(request)
        if request.method != 'POST':
            context['form'] = AddLogNoteForm()
        else:
            form = AddLogNoteForm(request.POST)
            if form.is_valid():
                try:
                    note = form.cleaned_data['note']
                    vendor = self.get_object(request, object_id)
                    vendor.reject(by_user=request.user, note=note)
                    self.message_user(request, 'Rejected Catalog', messages.SUCCESS)
                except ValidationError as e:
                    self.message_user(request, e.message, messages.ERROR)
            else:
                self.message_user(request, form.errors[0], messages.ERROR)
            return self.to_change_list()
        return TemplateResponse(request, 'admin/flashdeal/form_submit.html', context)


@admin.register(FlashDeal)
class FlashDealAdmin(admin.ModelAdmin):

    list_display = ('catalog', 'start_time', 'end_time', 'created_at')
    list_filter = ('catalog', )


