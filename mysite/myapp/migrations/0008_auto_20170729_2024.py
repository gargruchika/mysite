# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20170729_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='password',
            field=models.CharField(max_length=400),
        ),
    ]
