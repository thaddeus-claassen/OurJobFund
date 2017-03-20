# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-09 21:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobuser', '0004_auto_20170309_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledgenotification',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobuser.Comment'),
        ),
        migrations.AlterField(
            model_name='pledgenotification',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobuser.WorkJobUpdate'),
        ),
        migrations.AlterField(
            model_name='worknotification',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobuser.Comment'),
        ),
        migrations.AlterField(
            model_name='worknotification',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobuser.WorkJobUpdate'),
        ),
    ]
