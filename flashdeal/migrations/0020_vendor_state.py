# Generated by Django 2.2.1 on 2019-06-16 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashdeal', '0019_auto_20190616_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='state',
            field=models.CharField(choices=[('andhra-pradesh-hyderabad', 'Andhra Pradesh – Hyderabad'), ('arunachal-pradesh', 'Arunachal Pradesh'), ('assam', 'Assam'), ('bihar', 'Bihar'), ('chhattisgarh', 'Chhattisgarh'), ('goa', 'Goa'), ('gujarat', 'Gujarat'), ('haryana', 'Haryana'), ('himachal-pradesh', 'Himachal Pradesh'), ('jammu-and-kashmir', 'Jammu and Kashmir'), ('jharkhand', 'Jharkhand'), ('karnataka', 'Karnataka'), ('kerala', 'Kerala'), ('madhya-pradesh', 'Madhya Pradesh'), ('maharashtra', 'Maharashtra'), ('manipur', 'Manipur'), ('meghalaya', 'Meghalaya'), ('mizoram', 'Mizoram'), ('nagaland', 'Nagaland'), ('odisha', 'Odisha'), ('punjab', 'Punjab'), ('rajasthan', 'Rajasthan'), ('sikkim', 'Sikkim'), ('tamil-nadu', 'Tamil Nadu'), ('telangana', 'Telangana'), ('tripura', 'Tripura'), ('uttar-pradesh', 'Uttar Pradesh'), ('uttarakhand', 'Uttarakhand'), ('west-bengal', 'West Bengal'), ('andaman-and-nicobar-islands', 'Andaman and Nicobar Islands'), ('chandigarh', 'Chandigarh'), ('dadra-and-nagar-haveli', 'Dadra and Nagar Haveli'), ('daman-and-diu', 'Daman and Diu'), ('lakshadweep', 'Lakshadweep'), ('delhi', 'Delhi'), ('puducherry', 'Puducherry')], default='assam', max_length=500),
            preserve_default=False,
        ),
    ]