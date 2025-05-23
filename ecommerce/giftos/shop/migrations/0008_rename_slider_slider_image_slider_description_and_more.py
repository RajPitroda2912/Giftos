# Generated by Django 5.1.6 on 2025-03-03 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_slider'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slider',
            old_name='slider',
            new_name='image',
        ),
        migrations.AddField(
            model_name='slider',
            name='description',
            field=models.TextField(default='Image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slider',
            name='title',
            field=models.CharField(default='Description', max_length=250),
            preserve_default=False,
        ),
    ]
