# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_url', models.URLField(null=True, blank=True)),
                ('video_api_url', models.URLField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('embed_html', models.TextField(null=True, blank=True)),
                ('video_id', models.CharField(unique=True, max_length=150)),
                ('owner_name', models.CharField(max_length=200, null=True, blank=True)),
                ('owner_id', models.CharField(max_length=200, null=True, blank=True)),
                ('owner_url', models.URLField(null=True, blank=True)),
                ('thumbnail_url', models.URLField(null=True, blank=True)),
                ('title', models.CharField(max_length=300, null=True, blank=True)),
                ('views_total', models.IntegerField(null=True, blank=True)),
                ('related', models.ManyToManyField(related_name='related_rel_+', null=True, to='crawler.Video', blank=True)),
                ('site', models.ForeignKey(to='crawler.Site')),
                ('tags', models.ManyToManyField(to='crawler.Tag', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
