# Generated by Django 4.2 on 2023-05-09 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_product_is_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Occasion',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
    ]
