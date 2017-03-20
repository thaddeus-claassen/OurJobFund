# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-10 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobuser', '0005_auto_20170309_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pledgenotification',
            name='money_request',
        ),
        migrations.AddField(
            model_name='pledgenotification',
            name='jo_pk',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workjob',
            name='amount_of_money_asking_for',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
