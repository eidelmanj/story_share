# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story_site', '0010_compilation'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='durationSeconds',
            field=models.PositiveIntegerField(default=1000),
            preserve_default=False,
        ),
    ]
