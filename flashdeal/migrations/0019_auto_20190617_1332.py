# Generated by Django 2.2.1 on 2019-06-17 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0018_auto_20190617_1314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='product_variant',
            new_name='product_variants',
        ),
    ]
