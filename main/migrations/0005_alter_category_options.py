# Generated by Django 4.2 on 2023-05-09 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_banner_remove_product_price_productattribute'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]