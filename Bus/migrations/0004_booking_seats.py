# Generated by Django 3.0.8 on 2020-07-29 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bus', '0003_auto_20200729_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='seats',
            field=models.IntegerField(default=0),
        ),
    ]
