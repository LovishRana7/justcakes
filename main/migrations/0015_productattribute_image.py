# Generated by Django 4.2 on 2023-05-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_productreview_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattribute',
            name='image',
            field=models.ImageField(null=True, upload_to='product_imgs/'),
        ),
    ]
