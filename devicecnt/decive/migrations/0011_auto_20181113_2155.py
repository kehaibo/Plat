# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-13 21:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decive', '0010_auto_20181112_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='downstream',
            name='down_point',
        ),
        migrations.RemoveField(
            model_name='downstream',
            name='model_name',
        ),
    ]
