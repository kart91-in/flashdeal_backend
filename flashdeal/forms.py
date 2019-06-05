from django import forms
from django.urls import reverse

from flashdeal.models import Product, Image, Catalog, FlashDeal


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
    )
    sale_price = forms.DecimalField()
    upper_price = forms.DecimalField(required=False)
    catalogs = forms.ModelMultipleChoiceField(queryset=Catalog.objects.all())

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._image_list = kwargs.pop('_image_list', [])
        super().__init__(*args, **kwargs)
        self.fields['catalogs'].queryset = Catalog.objects.filter(
            vendor=self._user.vendor
        )

    def save(self, commit=True):
        self.instance.vendor = self._user.vendor
        super().save(commit)
        for image in self._image_list:
            self.instance.images.create(
                image=image,
                name=image.name,
                owner=self._user
            )


class CreateCatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('name', 'description', 'products', )

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._image_list = kwargs.pop('_image_list', [])
        self._video_list = kwargs.pop('_video_list', [])
        super().__init__(*args, **kwargs)
        self.fields['products'].queryset = Product.objects.filter(vendor=self._user.vendor)

    def save(self, commit=True):
        self.instance.vendor = self._user.vendor
        super().save(commit)
        for image in self._image_list:
            self.instance.images.create(
                image=image,
                name=image.name,
                owner=self._user
            )

        for video in self._video_list:
            self.instance.videos.create(
                video=video,
                name=video.name,
                owner=self._user
            )


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

