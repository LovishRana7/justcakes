# Generated by Django 4.2 on 2023-05-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_product_occasion_remove_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='img',
            field=models.ImageField(max_length=200, upload_to=''),
        ),
    ]
