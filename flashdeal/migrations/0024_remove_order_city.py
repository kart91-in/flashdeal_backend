# Generated by Django 2.2.1 on 2019-06-17 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0023_deliveryinfo_meta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
    ]
