# Generated by Django 4.2 on 2023-05-10 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_brand_to_occasion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='brand',
            new_name='occasion',
        ),
        migrations.AlterField(
            model_name='banner',
            name='img',
            field=models.ImageField(upload_to='banner_imgs/'),
        ),
        migrations.AlterField(
            model_name='occasion',
            name='image',
            field=models.ImageField(upload_to='occasion_imgs/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='occasion_images/'),
        ),
    ]