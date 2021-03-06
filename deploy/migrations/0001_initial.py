# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-01-31 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SaltHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_name', models.CharField(max_length=50, unique=True, verbose_name='\u4e3b\u673a\u540d\u79f0')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='\u4e3b\u673aIP')),
            ],
            options={
                'verbose_name': 'salt\u4e3b\u673a\u7ba1\u7406',
                'verbose_name_plural': 'salt\u4e3b\u673a\u7ba1\u7406',
            },
        ),
    ]
