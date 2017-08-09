# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-27 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userprofile_stripe_account_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_time_name_was_changed',
            field=models.DateTimeField(default='2000-01-01'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='stripe_account_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]