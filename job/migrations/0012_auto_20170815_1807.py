# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-15 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_auto_20170815_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='paid',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='pledged',
            field=models.PositiveIntegerField(default=0),
        ),
    ]