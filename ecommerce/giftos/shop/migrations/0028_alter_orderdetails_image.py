# Generated by Django 5.2 on 2025-04-12 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='image',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
