# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-12-04 15:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='\u673a\u623f\u540d\u5b57')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u673a\u623f\u5730\u5740')),
                ('type', models.CharField(choices=[('DX', '\u7535\u4fe1'), ('LT', '\u8054\u901a'), ('YD', '\u79fb\u52a8'), ('ZJ', '\u81ea\u5efa')], default='DX', max_length=20, verbose_name='\u673a\u623f\u7c7b\u578b')),
                ('bandwidth', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u673a\u623f\u5e26\u5bbd')),
                ('contact', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u8054\u7cfb\u4eba')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='\u90ae\u7bb1')),
            ],
            options={
                'verbose_name': '\u673a\u623f',
                'verbose_name_plural': '\u673a\u623f\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u8d44\u4ea7')),
                ('payment', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u652f\u4ed8\u65b9\u5f0f')),
                ('info', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u652f\u4ed8\u4fe1\u606f')),
                ('cost', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u7533\u8bf7\u5355\u91d1\u989d')),
                ('unit', models.IntegerField(blank=True, choices=[(1, '\u4eba\u6c11\u5e01 CNY'), (2, '\u6e2f\u5e01 HKD'), (3, '\u7f8e\u91d1 USD')], default=1, null=True, verbose_name='\u91d1\u989d\u5355\u4f4d')),
                ('payment_status', models.IntegerField(blank=True, choices=[(1, '\u5f85\u4ed8\u6b3e'), (2, '\u5df2\u4ed8\u6b3e'), (3, '\u5f85\u7eed\u8d39'), (4, '\u5df2\u7533\u8bf7\u7eed\u8d39')], default=1, null=True, verbose_name='\u4ed8\u6b3e\u72b6\u6001')),
                ('approve_status', models.IntegerField(blank=True, choices=[(1, '\u5f85\u5ba1\u6279'), (2, '\u5df2\u901a\u8fc7'), (3, '\u672a\u901a\u8fc7')], default=1, null=True, verbose_name='\u5ba1\u6279\u72b6\u6001')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('end_time', models.DateField(blank=True, null=True, verbose_name='\u8d44\u4ea7\u622a\u6b62\u65e5\u671f')),
                ('comment', models.TextField(blank=True, max_length=100, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'verbose_name': '\u7533\u8bf7\u5355',
                'verbose_name_plural': '\u7533\u8bf7\u5355\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='IP')),
                ('cabinet', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u673a\u67dc\u53f7')),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='\u673a\u5668\u4f4d\u7f6e')),
                ('status', models.IntegerField(blank=True, choices=[(1, '\u6b63\u5e38'), (2, '\u505c\u7528')], default=1, null=True, verbose_name='\u72b6\u6001')),
                ('buy_date', models.DateField(auto_now_add=True, null=True, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='\u5230\u671f\u65e5\u671f')),
                ('cost', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u8d2d\u4e70\u8d39\u7528')),
                ('use', models.TextField(blank=True, max_length=100, null=True, verbose_name='\u4f5c\u7528')),
                ('idc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assets.Idc', verbose_name='\u6240\u5c5e\u673a\u623f')),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668',
                'verbose_name_plural': '\u670d\u52a1\u5668\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='ServerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u4e3b\u673a\u540d')),
                ('hwaddr', models.CharField(blank=True, max_length=50, null=True, verbose_name='MAC\u5730\u5740')),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5382\u5546')),
                ('brand', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u4ea7\u54c1\u578b\u53f7')),
                ('cpu', models.CharField(blank=True, max_length=50, null=True, verbose_name='CPU\u578b\u53f7')),
                ('cpu_num', models.PositiveSmallIntegerField(verbose_name='CPU\u6838\u6570')),
                ('memory', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5185\u5b58')),
                ('disk', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u786c\u76d8')),
                ('system_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u7cfb\u7edf\u7c7b\u578b')),
                ('system_version', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u7cfb\u7edf\u7248\u672c')),
                ('system_arch', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u7cfb\u7edf\u5e73\u53f0')),
                ('type', models.IntegerField(blank=True, choices=[(1, '\u7269\u7406\u673a'), (2, '\u865a\u62df\u673a'), (3, '\u5bb9\u5668')], default=1, null=True, verbose_name='\u7c7b\u578b')),
                ('virtual', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u865a\u62df\u73af\u5883')),
                ('sn', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5e8f\u5217\u53f7')),
                ('ip', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Server', verbose_name='IP')),
                ('vm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assets.ServerInfo', verbose_name='\u5bbf\u4e3b\u673a')),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668\u4fe1\u606f',
                'verbose_name_plural': '\u670d\u52a1\u5668\u4fe1\u606f\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u670d\u52a1\u540d\u79f0')),
                ('use', models.TextField(blank=True, max_length=100, null=True, verbose_name='\u4f5c\u7528')),
                ('status', models.IntegerField(blank=True, choices=[(1, '\u6b63\u5e38'), (2, '\u505c\u7528')], default=1, null=True, verbose_name='\u72b6\u6001')),
                ('buy_date', models.DateField(auto_now_add=True, null=True, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='\u5230\u671f\u65e5\u671f')),
                ('cost', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u8d2d\u4e70\u8d39\u7528')),
            ],
            options={
                'verbose_name': '\u670d\u52a1',
                'verbose_name_plural': '\u670d\u52a1\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='\u4f9b\u5e94\u5546\u540d\u79f0')),
                ('website', models.CharField(blank=True, max_length=100, null=True, verbose_name='\u7f51\u7ad9')),
                ('contact', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u8054\u7cfb\u4eba')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='\u90ae\u7bb1')),
                ('comment', models.TextField(blank=True, max_length=100, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'verbose_name': '\u4f9b\u5e94\u5546',
                'verbose_name_plural': '\u4f9b\u5e94\u5546\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='\u7c7b\u578b\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u7c7b\u578b',
                'verbose_name_plural': '\u670d\u52a1\u7c7b\u578b\u5217\u8868',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assets.Supplier', verbose_name='\u4f9b\u5e94\u5546'),
        ),
        migrations.AddField(
            model_name='service',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Type', verbose_name='\u670d\u52a1\u7c7b\u578b'),
        ),
    ]
