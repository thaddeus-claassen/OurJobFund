# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-29 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_time_worked_on', models.DateTimeField(auto_now_add=True)),
                ('money_pledged', models.FloatField(default='0.0')),
                ('num_people_doing_job', models.IntegerField(default='0')),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('description', models.CharField(default='', max_length=10000)),
            ],
        ),
        migrations.AddField(
            model_name='hashtag',
            name='jobs',
            field=models.ManyToManyField(to='JobList.Job'),
        ),
    ]
