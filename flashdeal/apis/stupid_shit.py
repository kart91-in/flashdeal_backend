import pandas as pd
import numpy as np
import random
from django.conf import settings
import os

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

save_path = settings.MEDIA_ROOT + 'charts'
if not os.path.isdir(save_path):
    os.mkdir(save_path, 0o755)

class ContactAPI(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        return Response({'info': 'Email - info@kart91.in;  Phone No - 9780-96-9780'}, status=status.HTTP_200_OK)


class ChartFileListAPI(ListAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        charts = _url_list()
        return Response({'charts': charts}, status=status.HTTP_200_OK)

def _url_list():
    return [f'{settings.MEDIA_URL}charts/{name}' for name in get_all_chart_files()]

def get_all_chart_files():
    return os.listdir(save_path)

def vendor_charts():
    company_name = list(range(3))
    phone = []
    bank_acc = []
    uid = []

    for i in range(3):
        phone.append(random.randint(6500000000,9999999999))
        bank_acc.append(random.randint(0,99999999999))
        uid.append(random.randint(0,9999))
    register = pd.DataFrame({'Vendor_ID':uid, 'company_name':company_name,'phone':phone,'bank_account':bank_acc})

    SKUs = []
    sku_id = []
    image = []
    vid = []
    cat = []
    amount = []
    timestamp = []
    tor = []
    tod = []
    tot = []
    tore = []
    size = []
    profit = []
    colour = []
    for i in range(3):
        SKUs.append(pd.DataFrame({'Timestamp':timestamp,'SKU_Id':sku_id, 'image':image, 'video':vid, 'Catalog':cat, 'Colour':colour,
                                 'Amount sold':amount, 'Profit':profit,'total_orders_recieved':tor,'total_orders_dispatched':tod,
                                 'total_orders_in_transit':tot, 'total_orders_returned':tore,'Size':size}))

    sku_register = pd.DataFrame({'id':register.phone,'SKUs':SKUs})
    sku_register.set_index('id', inplace = True)

    phone_number = []
    #change the number of range from 3 to any value depending on the number of vendors to visualize
    for i in range(len(sku_register)):
        phone_number.append(sku_register.index[i])

    for i in phone_number:
        sku_register.SKUs[i].Timestamp = pd.date_range(pd.datetime.today(), periods=1000).tolist()

    for i in phone_number:
        sku_register.SKUs[i].SKU_Id = [random.choice(list(range(50))) for i in range(1000)]
        sku_register.SKUs[i]['Amount sold'] = [random.randint(0,250) for i in range(1000)]
        sku_register.SKUs[i]['Catalog'] = [random.choice(['A', 'B', 'C', 'D', 'E', 'F']) for i in range(1000)]
        sku_register.SKUs[i]['Colour'] = [random.choice(['Red', 'Blue', 'Indigo', 'Maroon', 'Yellow']) for i in range(1000)]
        sku_register.SKUs[i]['Profit'] = [np.random.normal(0, 0.1, 1)[0]*10000 for i in range(1000)]
        sku_register.SKUs[i]['total_orders_recieved'] = sku_register.SKUs[i]['Amount sold'] + pd.DataFrame([random.randint(0,100) for i in range(1000)])
        sku_register.SKUs[i]['total_orders_dispatched'] = sku_register.SKUs[i]['Amount sold']
        sku_register.SKUs[i]['total_orders_in_transit'] = [random.randint(0,250) for i in range(1000)]
        sku_register.SKUs[i]['total_orders_returned'] = sku_register.SKUs[i]['total_orders_recieved'] - sku_register.SKUs[i]['Amount sold']
        sku_register.SKUs[i]['Size'] = [random.choice(['s','m', 'l', 'xl', 'xxl']) for i in range(1000)]

    import seaborn as sns
    import matplotlib.pyplot as plt

    for i in phone_number:
        sku_register.SKUs[i]['day'] = sku_register.SKUs[i].Timestamp.dt.day
        sku_register.SKUs[i]['week'] = sku_register.SKUs[i].Timestamp.dt.week
        sku_register.SKUs[i]['month'] = sku_register.SKUs[i].Timestamp.dt.month
        sku_register.SKUs[i]['hour'] = sku_register.SKUs[i].Timestamp.dt.month

    for i in phone_number:
        plt.figure(figsize = (14,10))
        plt.title('SKU wise profit for vendor' + str(i))
        figplt = sns.boxplot(sku_register.SKUs[i].SKU_Id, sku_register.SKUs[i].Profit)
        figplt.get_figure().savefig(f'{save_path}/vendor_profit_{i}')

        plt.figure(figsize = (14,10))
        plt.title('SKU wise amount sold for vendor' + str(i))
        figplt1 = sns.boxplot(sku_register.SKUs[i].SKU_Id, sku_register.SKUs[i]['Amount sold'])
        figplt1.get_figure().savefig(f'{save_path}/vendor_sold_{i}')

    for i in phone_number:
        plt.figure(figsize=(14, 10))
        plt.title('SKU wise orders recieved for vendor' + str(i))
        figplt2 = sns.boxplot(sku_register.SKUs[i].SKU_Id, sku_register.SKUs[i].total_orders_recieved)
        figplt2.get_figure().savefig(f'{save_path}/order_recieved_{i}')

        plt.figure(figsize=(14, 10))
        plt.title('SKU wise orders dispatched for vendor' + str(i))
        figplt3 = sns.boxplot(sku_register.SKUs[i].SKU_Id, sku_register.SKUs[i].total_orders_dispatched)
        figplt3.get_figure().savefig(f'{save_path}/order_dispatched_{i}')

        plt.figure(figsize=(14, 10))
        plt.title('SKU wise total orders in transit for vendor' + str(i))
        figplt4 = sns.boxplot(sku_register.SKUs[i].SKU_Id, sku_register.SKUs[i].total_orders_in_transit)
        figplt4.get_figure().savefig(f'{save_path}/order_transit_{i}')

        plt.figure(figsize=(14, 10))
        plt.title('SKU wise total orders returned for vendor' + str(i))
        figplt5 = sns.boxplot(sku_register.SKUs[i].SKU_Id, sku_register.SKUs[i].total_orders_returned)
        figplt5.get_figure().savefig(f'{save_path}/order_returned_{i}')


    for i in phone_number:
        weekly_sales = pd.DataFrame(sku_register.SKUs[i].groupby(['week'])['Amount sold'].sum())
        plt.title('Weekly amount trend for vendor' + str(i))
        figplt6 = plt.plot(weekly_sales['Amount sold'])[0]
        figplt6.get_figure().savefig(f'{save_path}/amount_sold_{i}')

        weekly_profit = pd.DataFrame(sku_register.SKUs[i].groupby(['week'])['Profit'].sum())
        plt.title('Weekly profit trend for vendor' + str(i))
        figplt7 = plt.plot(weekly_profit['Profit'])[0]
        figplt7.get_figure().savefig(f'{save_path}/profit_{i}')

    for i in phone_number:
        daily_sales = pd.DataFrame(sku_register.SKUs[i].groupby(['day'])['Amount sold'].sum())
        plt.title('Day-wise amount trend for vendor' + str(i))
        figplt8 = plt.plot(daily_sales['Amount sold'])[0]
        figplt8.get_figure().savefig(f'{save_path}/day_sold_{i}')

        daily_profit = pd.DataFrame(sku_register.SKUs[i].groupby(['day'])['Profit'].sum())
        plt.title('Day-wise profit trend for vendor' + str(i))
        figplt9 = plt.plot(daily_profit['Profit'])[0]
        figplt9.get_figure().savefig(f'{save_path}/day_profit_{i}')

    for i in phone_number:
        hourly_sales = pd.DataFrame(sku_register.SKUs[i].groupby(['hour'])['Amount sold'].sum())
        plt.title('Hourly amount trend for vendor' + str(i))
        figplt10 = plt.plot(hourly_sales['Amount sold'])[0]
        figplt10.get_figure().savefig(f'{save_path}/hour_sold_{i}')

        hourly_profit = pd.DataFrame(sku_register.SKUs[i].groupby(['hour'])['Profit'].sum())
        plt.title('Hourly profit trend for vendor' + str(i))
        figplt11 = plt.plot(hourly_profit['Profit'])[0]
        figplt11.get_figure().savefig(f'{save_path}/hour_profit_{i}')

    for i in phone_number:
        catalog_sales = pd.DataFrame(sku_register.SKUs[i].groupby(['Catalog'])['Amount sold'].sum())
        catalog_sales.reset_index(level=0, inplace=True)
        plt.title('Catalog amount trend for vendor' + str(i))
        figplt12 = sns.barplot(catalog_sales.Catalog, catalog_sales['Amount sold'])
        figplt12.get_figure().savefig(f'{save_path}/catalog_trending_{i}')

        catalog_profit = pd.DataFrame(sku_register.SKUs[i].groupby(['Catalog'])['Profit'].sum())
        catalog_profit.reset_index(level=0, inplace=True)
        plt.title('Catalog profit trend for vendor' + str(i))
        figplt13 = sns.barplot(catalog_profit.Catalog, catalog_profit['Profit'])
        figplt13.get_figure().savefig(f'{save_path}/catalog_profit_{i}')

    for i in phone_number:
        color_sales = pd.DataFrame(sku_register.SKUs[i].groupby(['Colour'])['Amount sold'].sum())
        color_sales.reset_index(level=0, inplace=True)
        plt.title('Colour amount trend for vendor' + str(i))
        figplt14 = sns.barplot(color_sales.Colour, color_sales['Amount sold'])
        figplt14.get_figure().savefig(f'{save_path}/color_trending_{i}')

        color_profit = pd.DataFrame(sku_register.SKUs[i].groupby(['Colour'])['Profit'].sum())
        color_profit.reset_index(level=0, inplace=True)
        plt.title('Colour profit trend for vendor' + str(i))
        figplt15 = sns.barplot(color_profit.Colour, color_profit['Profit'])
        figplt15.get_figure().savefig(f'{save_path}/color_profit_{i}')

    for i in phone_number:
        size_sales = pd.DataFrame(sku_register.SKUs[i].groupby(['Size'])['Amount sold'].sum())
        size_sales.reset_index(level=0, inplace=True)
        plt.title('Size amount trend for vendor' + str(i))
        figplt16 = sns.barplot(size_sales.Size, size_sales['Amount sold'])
        figplt16.get_figure().savefig(f'{save_path}/size_trending_{i}')

        size_profit = pd.DataFrame(sku_register.SKUs[i].groupby(['Size'])['Profit'].sum())
        size_profit.reset_index(level=0, inplace=True)
        plt.title('Size profit trend for vendor' + str(i))
        figplt17 = sns.barplot(size_profit.Size, size_profit['Profit'])
        figplt17.get_figure().savefig(f'{save_path}/size_profit_{i}')

    for i in phone_number:
        sku_register.SKUs[i]['phone_number'] = pd.DataFrame({'phone_number': [i] * len(sku_register.SKUs[i])})

    complete_data = pd.concat([sku_register.SKUs[i] for i in phone_number])

    plt.title('Vendor-wise sold vs returned')
    figplt18 = sns.barplot(complete_data.phone_number, complete_data['Amount sold'])
    figplt18.get_figure().savefig(f'{save_path}/overall_sold_vs_return')

    plt.title('Vendor-wise sold vs returned')
    figplt19 = sns.barplot(complete_data.phone_number, complete_data.total_orders_returned)
    figplt19.get_figure().savefig(f'{save_path}/overall_sold_vs_return')

