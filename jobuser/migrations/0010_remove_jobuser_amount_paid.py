# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-01 16:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobuser', '0009_auto_20170626_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobuser',
            name='amount_paid',
        ),
    ]
