# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('story_site', '0016_auto_20150619_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalStoryRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.DecimalField(max_digits=5, decimal_places=3)),
                ('story', models.ForeignKey(to='story_site.Story')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='story',
            name='numVotes',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
