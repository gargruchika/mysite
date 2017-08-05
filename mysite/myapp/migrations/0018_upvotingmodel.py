# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_postmodel_has_liked'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpvotingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.CommentModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.UserModel')),
            ],
        ),
    ]
