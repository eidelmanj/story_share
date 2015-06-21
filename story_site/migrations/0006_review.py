# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story_site', '0005_story_averagerank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=100)),
                ('review', models.CharField(max_length=2000)),
                ('stars', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
