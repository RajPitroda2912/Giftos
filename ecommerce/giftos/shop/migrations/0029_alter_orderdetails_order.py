# Generated by Django 5.2 on 2025-04-12 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_alter_orderdetails_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='shop.order'),
        ),
    ]
