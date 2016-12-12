# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-12 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0003_messagelog_message_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(default='-', max_length=255),
        ),
        migrations.AddField(
            model_name='message',
            name='to_address',
            field=models.CharField(default='-', max_length=255),
        ),
        migrations.AddField(
            model_name='messagelog',
            name='title',
            field=models.CharField(default='-', max_length=255),
        ),
        migrations.AddField(
            model_name='messagelog',
            name='to_address',
            field=models.CharField(default='-', max_length=255),
        ),
    ]
