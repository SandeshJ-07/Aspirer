# Generated by Django 3.2.7 on 2021-11-05 10:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0005_auto_20211105_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='Profile',
        ),
        migrations.RemoveField(
            model_name='post',
            name='profile',
        ),
        migrations.AlterField(
            model_name='comment',
            name='uploadTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 16, 26, 37, 517955)),
        ),
        migrations.AlterField(
            model_name='post',
            name='uploadTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 16, 26, 37, 517955)),
        ),
    ]
