# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 04:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20170730_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessiontoken',
            name='session_token',
            field=models.CharField(max_length=255),
        ),
    ]
