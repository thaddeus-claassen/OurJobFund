# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finish',
            name='jobuser',
        ),
        migrations.AddField(
            model_name='work',
            name='status',
            field=models.CharField(choices=[('working', 'working'), ('finished', 'finished')], default='working', max_length=10),
        ),
        migrations.DeleteModel(
            name='Finish',
        ),
    ]