# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserViewedPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-when_posted']},
        ),
        migrations.AddField(
            model_name='post',
            name='when_posted',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 16, 1, 24, 51, 302000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userviewedpost',
            name='post',
            field=models.ForeignKey(related_name='viewed_post_set', to='home.Post'),
        ),
        migrations.AddField(
            model_name='userviewedpost',
            name='user',
            field=models.ForeignKey(related_name='viewed_post_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
