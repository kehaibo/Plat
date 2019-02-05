# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-18 22:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='data_point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_name', models.CharField(max_length=64)),
                ('show_name', models.CharField(max_length=64)),
                ('TLV_Type', models.CharField(default='', max_length=4)),
                ('operation_type', models.CharField(max_length=2)),
                ('data_type', models.CharField(max_length=12)),
                ('max_value', models.CharField(blank=True, max_length=64)),
                ('min_value', models.CharField(blank=True, max_length=64)),
                ('step_by_step', models.CharField(blank=True, max_length=64)),
                ('value_unit', models.CharField(max_length=12)),
                ('true_value_name', models.CharField(blank=True, max_length=64)),
                ('true_value_show', models.CharField(blank=True, max_length=64)),
                ('true_bool_value', models.NullBooleanField()),
                ('false_value_name', models.CharField(blank=True, max_length=64)),
                ('false_value_show', models.CharField(blank=True, max_length=64)),
                ('false_bool_value', models.NullBooleanField()),
                ('str_maxlen', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Deviceinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UUID', models.CharField(blank=True, max_length=32)),
                ('device_name', models.CharField(blank=True, max_length=64)),
                ('device_class', models.CharField(blank=True, max_length=64)),
                ('device_desc', models.CharField(default='', max_length=100)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('device_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UUID', models.CharField(blank=True, max_length=32)),
                ('status', models.CharField(blank=True, max_length=1)),
                ('info', models.CharField(blank=True, max_length=10)),
                ('currenttime', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.Deviceinfo')),
            ],
        ),
        migrations.CreateModel(
            name='downstream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream_showname', models.CharField(default='', max_length=64)),
                ('stream_name', models.CharField(default='', max_length=64)),
                ('stream_Type', models.CharField(default='', max_length=4)),
                ('stream_len', models.CharField(default='', max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='downstream_datapoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_attr', models.CharField(default='', max_length=1)),
                ('data_point', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.data_point')),
                ('downstream', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.downstream')),
            ],
        ),
        migrations.CreateModel(
            name='ProductModelName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_model', models.CharField(max_length=64, unique=True)),
                ('product_desc', models.CharField(blank=True, max_length=64)),
                ('current_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('protocol_type', models.CharField(default='', max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='upstream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream_showname', models.CharField(default='', max_length=64)),
                ('stream_name', models.CharField(default='', max_length=64)),
                ('stream_Type', models.CharField(default='', max_length=4)),
                ('stream_len', models.CharField(default='', max_length=4)),
                ('model_name', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.ProductModelName')),
            ],
        ),
        migrations.CreateModel(
            name='upstream_datapoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_attr', models.CharField(default='', max_length=1)),
                ('data_point', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.data_point')),
                ('model_name', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.ProductModelName')),
                ('upstream', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.upstream')),
            ],
        ),
        migrations.AddField(
            model_name='downstream_datapoint',
            name='model_name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.ProductModelName'),
        ),
        migrations.AddField(
            model_name='downstream',
            name='model_name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.ProductModelName'),
        ),
        migrations.AddField(
            model_name='deviceinfo',
            name='model_name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.ProductModelName'),
        ),
        migrations.AddField(
            model_name='data_point',
            name='model_name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='decive.ProductModelName'),
        ),
    ]