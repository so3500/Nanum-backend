# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import issue.models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_auto_20160617_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuefile',
            name='unique_name',
        ),
        migrations.AlterField(
            model_name='issue',
            name='comment_count',
            field=models.IntegerField(default=0, help_text='댓글 수'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='contents',
            field=models.TextField(blank=True, help_text='내용'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='count',
            field=models.IntegerField(default=0, help_text='조회수'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, help_text='작성일'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='like_count',
            field=models.IntegerField(default=0, help_text='좋아요 개수'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='likes',
            field=models.ManyToManyField(help_text='좋아요', related_name='issue_likes', through='issue.IssueLike', to='accounts.NanumUser'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(help_text='해시 태그', to='issue.IssueTag'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='thumbnail',
            field=models.ImageField(help_text='프로필 사진', null=True, upload_to=issue.models.get_issue_thumbnail_path),
        ),
        migrations.AlterField(
            model_name='issue',
            name='title',
            field=models.CharField(blank=True, help_text='제목', max_length=200),
        ),
        migrations.AlterField(
            model_name='issue',
            name='update_date',
            field=models.DateTimeField(auto_now=True, help_text='수정일'),
        ),
        migrations.AlterField(
            model_name='issuecomment',
            name='contents',
            field=models.TextField(blank=True, help_text='내용'),
        ),
        migrations.AlterField(
            model_name='issuecomment',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, help_text='작성일'),
        ),
        migrations.AlterField(
            model_name='issuecomment',
            name='update_date',
            field=models.DateTimeField(auto_now=True, help_text='수정일'),
        ),
        migrations.AlterField(
            model_name='issuecomment',
            name='user',
            field=models.ForeignKey(help_text='작성자', on_delete=django.db.models.deletion.CASCADE, related_name='issue_comment_users', to='accounts.NanumUser'),
        ),
        migrations.AlterField(
            model_name='issuefile',
            name='attached_file',
            field=models.FileField(help_text='첨부 파일', null=True, upload_to=issue.models.get_issue_file_path),
        ),
        migrations.AlterField(
            model_name='issuefile',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, help_text='생성일'),
        ),
        migrations.AlterField(
            model_name='issuefile',
            name='download_count',
            field=models.IntegerField(default=0, help_text='다운로드 횟수'),
        ),
        migrations.AlterField(
            model_name='issuefile',
            name='name',
            field=models.CharField(help_text='파일 이름', max_length=200),
        ),
        migrations.AlterField(
            model_name='issuefile',
            name='size',
            field=models.CharField(help_text='파일 크기(kb) in char type', max_length=200),
        ),
        migrations.AlterField(
            model_name='issuefile',
            name='update_date',
            field=models.DateTimeField(auto_now=True, help_text='수정일'),
        ),
        migrations.AlterField(
            model_name='issuelike',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, help_text='좋아요 클릭 시간'),
        ),
        migrations.AlterField(
            model_name='issuetag',
            name='name',
            field=models.CharField(help_text='해시 태그 이름', max_length=50, unique=True),
        ),
    ]