# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 04:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import issue.models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0004_auto_20160621_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='해시 태그', to='issue.IssueTag'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='thumbnail',
            field=models.ImageField(blank=True, help_text='프로필 사진', null=True, upload_to=issue.models.get_issue_thumbnail_path),
        ),
        migrations.AlterField(
            model_name='issue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_users', to='accounts.NanumUser'),
        ),
    ]
