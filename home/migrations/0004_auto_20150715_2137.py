# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20150715_2028'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userviewedpost',
            unique_together=set([('user', 'post')]),
        ),
    ]
