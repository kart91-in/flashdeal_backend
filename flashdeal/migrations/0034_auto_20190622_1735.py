# Generated by Django 2.2.2 on 2019-06-22 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0033_vendor_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='product_variants',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_variants',
        ),
        migrations.CreateModel(
            name='ProductVariantOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', related_query_name='purchase', to='flashdeal.Order')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashdeal.ProductVariant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductVariantBasket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField(default=1)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', related_query_name='purchase', to='flashdeal.Basket')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashdeal.ProductVariant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]