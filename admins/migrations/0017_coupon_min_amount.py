# Generated by Django 4.1.1 on 2022-10-22 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0016_remove_offers_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='min_amount',
            field=models.IntegerField(default=0),
        ),
    ]
