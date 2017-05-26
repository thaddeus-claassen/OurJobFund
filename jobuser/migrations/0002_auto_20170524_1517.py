# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-24 20:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0002_auto_20170523_1656'),
        ('jobuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=100)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='commenter',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='job',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='update',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='job',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='notifier',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='update',
        ),
        migrations.RemoveField(
            model_name='workjobupdate',
            name='workjob',
        ),
        migrations.RemoveField(
            model_name='imageupload',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='imageupload',
            name='workJobUpdate',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
        migrations.DeleteModel(
            name='WorkJobUpdate',
        ),
    ]
