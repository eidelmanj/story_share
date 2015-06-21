# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story_site', '0015_auto_20150619_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='compilation',
            name='averageRank',
            field=models.DecimalField(default=1, max_digits=5, decimal_places=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compilation',
            name='numVotes',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
