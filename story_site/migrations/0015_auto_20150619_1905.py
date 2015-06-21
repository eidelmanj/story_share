# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story_site', '0014_personalcompilationrank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalcompilationrank',
            name='story',
        ),
        migrations.AddField(
            model_name='personalcompilationrank',
            name='compilation',
            field=models.ForeignKey(default=1, to='story_site.Compilation'),
            preserve_default=False,
        ),
    ]
