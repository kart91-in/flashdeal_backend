# Generated by Django 2.2.2 on 2019-06-22 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0034_auto_20190622_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='product_variants',
            field=models.ManyToManyField(through='flashdeal.ProductVariantBasket', to='flashdeal.ProductVariant'),
        ),
    ]