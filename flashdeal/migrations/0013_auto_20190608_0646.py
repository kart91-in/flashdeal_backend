# Generated by Django 2.2.1 on 2019-06-08 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0012_auto_20190608_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSizeStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock', models.PositiveSmallIntegerField(default=0)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashdeal.Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashdeal.Product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashdeal.ProductSize')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='products', related_query_name='product', through='flashdeal.ProductSizeStock', to='flashdeal.Image'),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, related_name='products', related_query_name='product', through='flashdeal.ProductSizeStock', to='flashdeal.ProductSize'),
        ),
    ]