# Generated by Django 4.1.1 on 2022-09-29 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]
