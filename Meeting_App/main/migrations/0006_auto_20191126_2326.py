# Generated by Django 2.2.7 on 2019-11-26 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20191124_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='token',
        ),
        migrations.AddField(
            model_name='meeting',
            name='token',
            field=models.CharField(default=12, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guest',
            name='check_in_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 26, 23, 26, 7, 342531)),
        ),
    ]
