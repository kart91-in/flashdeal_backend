from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.utils.html import format_html
from flashdeal.forms import AddLogNoteForm
from flashdeal.models import Vendor, VendorApprovalLog


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

        return format_html(f'<a class="button" href="{approve}">Approve</a> '
                           f'<a class="button danger" href="{reject}">Reject</a> ')

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
        return TemplateResponse(request, 'admin/flashdeal/vendor/form_submit.html', context)


@admin.register(VendorApprovalLog)
class VendorApprovalLogAdmin(admin.ModelAdmin):

    list_display = ('vendor', 'type', 'by_user', 'note', 'created_at')

    def by_user(self, obj):
        return obj.user