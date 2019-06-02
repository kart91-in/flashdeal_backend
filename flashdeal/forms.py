from django import forms
from flashdeal.models import Product, Image, Catalog


class AddLogNoteForm(forms.Form):

    note = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text='Add reason for your decision if you have one'
    )


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'sale_price', 'upper_price',)

    name = forms.CharField()
    description = forms.CharField(
        widget=forms.Textarea,
        help_text='Add reason for your decision if you have one')
    sale_price = forms.DecimalField()
    upper_price = forms.DecimalField(required=False)
    catalogs = forms.ModelMultipleChoiceField(queryset=Catalog.objects.all())

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['catalogs'].queryset = Catalog.objects.filter(vendor=self._user.vendor)

    def save(self, commit=True):
        super().save(commit)
        if hasattr(self, '_image_list'):
            for image in self._image_list:
                self.instance.images.create(
                    image=image,
                    name=image.name,
                    owner=self.instance.vendor.user
                )


class CreateCatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('name', 'description', 'products', )

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._image_list = kwargs.pop('_image_list')
        super().__init__(*args, **kwargs)
        self.fields['products'].queryset = Product.objects.filter(vendor=self._user.vendor)

    def save(self, commit=True):
        self.instance.vendor = self._user.vendor
        super().save(commit)
        if hasattr(self, '_image_list'):
            for image in self._image_list:
                self.instance.images.create(
                    image=image,
                    name=image.name,
                    owner=self.instance.vendor.user
                )