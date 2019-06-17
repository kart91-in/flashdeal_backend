# Generated by Django 2.2.1 on 2019-06-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0019_auto_20190617_1332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product_variant',
            new_name='product_variants',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tracking',
        ),
        migrations.AlterField(
            model_name='order',
            name='address_type',
            field=models.CharField(choices=[('home', 'home'), ('office', 'office')], default='home', max_length=500),
        ),
        migrations.AlterField(
            model_name='order',
            name='pin_code',
            field=models.CharField(max_length=6),
        ),
    ]
