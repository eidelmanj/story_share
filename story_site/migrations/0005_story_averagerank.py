# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story_site', '0004_auto_20150506_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='averageRank',
            field=models.DecimalField(default=5.0, max_digits=5, decimal_places=3),
            preserve_default=False,
        ),
    ]
