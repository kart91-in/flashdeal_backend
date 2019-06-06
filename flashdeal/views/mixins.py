from django.urls import reverse


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
                    },
                    # {
                    #     6text': 'Flash Deal list',
                    #     'url': reverse('flashdeal:flashdeal_list'),
                    # },
                    # {
                    #     'text': 'Create a Flash Deal',
                    #     'url': reverse('flashdeal:flashdeal_create'),
                    # },
                ]
            },
        ]

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['app_list'] = self.get_leftbar_apps()
        return super().get_context_data(**kwargs)
