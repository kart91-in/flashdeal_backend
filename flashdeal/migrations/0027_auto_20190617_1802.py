# Generated by Django 2.2.1 on 2019-06-17 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0026_awbnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_info',
        ),
        migrations.DeleteModel(
            name='DeliveryInfo',
        ),
    ]
