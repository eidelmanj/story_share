# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story_site', '0003_userprofile_birthdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('story', models.ForeignKey(to='story_site.Story')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='story',
            name='event',
            field=models.ForeignKey(default=1, to='story_site.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.ForeignKey(default=1, to='story_site.City'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.ForeignKey(default=1, to='story_site.Country'),
            preserve_default=False,
        ),
    ]
