# Generated by Django 3.2.7 on 2021-11-05 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_auto_20211105_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='uploadTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 16, 30, 35, 838629)),
        ),
        migrations.AlterField(
            model_name='post',
            name='uploadTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 16, 30, 35, 838629)),
        ),
    ]
