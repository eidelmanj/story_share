# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story_site', '0011_story_durationseconds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='durationSeconds',
        ),
        migrations.AddField(
            model_name='ownedaudiofile',
            name='duration',
            field=models.PositiveIntegerField(default=1000),
            preserve_default=False,
        ),
    ]
