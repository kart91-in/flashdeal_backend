# Generated by Django 2.2.1 on 2019-06-02 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0004_auto_20190602_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='catalogs', related_query_name='catalog', to='flashdeal.Product'),
        ),
    ]
