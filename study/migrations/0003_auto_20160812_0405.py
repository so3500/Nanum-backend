# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-12 04:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160709_0430'),
        ('study', '0002_auto_20160727_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', through='study.Like', to='accounts.NanumUser'),
        ),
        migrations.AddField(
            model_name='study',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', through='study.Member', to='accounts.NanumUser'),
        ),
        migrations.RemoveField(
            model_name='calendercategory',
            name='calender',
        ),
        migrations.AddField(
            model_name='calendercategory',
            name='calender',
            field=models.ManyToManyField(help_text='일정 정보', to='study.Calender'),
        ),
    ]
