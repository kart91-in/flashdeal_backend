from django import forms
from django.db import transaction
from django.urls import reverse

from flashdeal.models import Product, Image, Catalog, FlashDeal
from flashdeal.models.product_models import ProductColor, ProductSize


class AddLogNoteForm(forms.Form):

    note = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text='Add reason for your decision if you have one'
    )


class MetaFieldMixin(object):
    """
    Underscore will be added to the fields
    """
    meta_fields = ('user', )

    def __init__(self, *args, **kwargs):
        for field in self.meta_fields:
            setattr(self, f'_{field}', kwargs.pop(field, None))
        super().__init__(*args, **kwargs)


class CreateProductForm(MetaFieldMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'sale_price', 'upper_price', 'colors')

    name = forms.CharField()
    description = forms.CharField()
    sale_price = forms.DecimalField()
    upper_price = forms.DecimalField(required=False)
    catalogs = forms.ModelMultipleChoiceField(queryset=Catalog.objects, required=False)

    colors = forms.ModelMultipleChoiceField(queryset=ProductColor.objects)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['catalogs'].queryset = Catalog.objects.filter(
            vendor=self._user.vendor
        )

    def clean(self):
        print(self.data)
        cleaned_data = super().clean()
        size_list = []
        stock_list = []
        self.image_list = self.files.getlist('image_list')
        for i in range(len(self.image_list)):
            size_list.append(self.data.get(f'size_image_{i}'))
            stock_list.append(self.data.get(f'stock_image_{i}'))
        self.size_list = size_list
        self.stock_list = stock_list
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        self.instance.vendor = self._user.vendor
        super().save(commit)
        for i in range(len(self.image_list)):
            image_file = self.image_list[i]
            image = Image.objects.create(
                image=image_file,
                name=image_file.name,
                owner=self._user
            )
            self.instance.images.add(image)
        return self.instance


class CreateCatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('name', 'description', 'products', )

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['products'].queryset = Product.objects.filter(vendor=self._user.vendor)

    def save(self, commit=True):
        self.instance.vendor = self._user.vendor
        super().save(commit)
        return self.instance



class CreateFlashDealForm(forms.ModelForm):
    class Meta:
        model = FlashDeal
        fields = ('catalog', 'start_time', 'end_time')

    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)

    def __init__(self, *args, **kwargs):
        print(kwargs)
        self._user = kwargs.pop('user')
        catalog_id = kwargs.pop('catalog_id', None)
        super().__init__(*args, **kwargs)
        self.fields['catalog'].queryset = Catalog.objects.filter(
            vendor=self._user.vendor, status=Catalog.STATUS_VERIFIED
        )
        if catalog_id:
            self.fields['catalog'].initial = Catalog.objects.get(id=catalog_id)

