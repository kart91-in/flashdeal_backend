# Generated by Django 2.2.2 on 2019-06-23 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0036_order_product_variants'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnorder',
            name='reason',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
