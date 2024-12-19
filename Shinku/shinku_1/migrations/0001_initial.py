# Generated by Django 5.1.2 on 2024-12-10 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='主要总类')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='组名')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('email', models.CharField(max_length=20, verbose_name='邮箱')),
                ('status', models.SmallIntegerField(choices=[(1, '使用中'), (2, '已注销')], default=1, verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='商品名称')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('description', models.CharField(max_length=100, verbose_name='商品描述')),
                ('main_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shinku_1.maintype')),
            ],
        ),
    ]
