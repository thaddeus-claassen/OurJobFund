# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-14 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20170914_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterworkers',
            name='not_been_active_in_the_last_n_days',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
