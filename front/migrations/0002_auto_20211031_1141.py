# Generated by Django 3.2.7 on 2021-10-31 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='acc_type',
        ),
        migrations.AddField(
            model_name='profile',
            name='pvt_acc',
            field=models.BooleanField(default=False),
        ),
    ]
