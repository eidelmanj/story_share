# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('story_site', '0002_userkind_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(default=datetime.datetime(2015, 5, 6, 6, 51, 4, 617880, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
