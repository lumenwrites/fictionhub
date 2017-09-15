# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-14 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0002_auto_20170614_0456'),
        ('profiles', '0002_user_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='purchased_series',
            field=models.ManyToManyField(blank=True, related_name='purchased_by', to='series.Series'),
        ),
    ]
