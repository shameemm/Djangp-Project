# Generated by Django 4.1.1 on 2022-09-30 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0006_rename_image_product_image1_product_image2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image1',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image3',
        ),
    ]
