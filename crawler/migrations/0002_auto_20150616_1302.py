# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='site',
        ),
        migrations.DeleteModel(
            name='Site',
        ),
        migrations.RemoveField(
            model_name='video',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
