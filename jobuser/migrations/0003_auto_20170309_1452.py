# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-09 20:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobuser', '0002_pledgenotification_worknotification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pledgenotification',
            old_name='user',
            new_name='pledger',
        ),
        migrations.RenameField(
            model_name='worknotification',
            old_name='user',
            new_name='worker',
        ),
    ]
