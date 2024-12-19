# Generated by Django 5.1.2 on 2024-12-12 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shinku_1', '0012_order_good'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '商品下架'), (1, '商品上架'), (2, '商品被ban')], default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '封禁'), (1, '使用中'), (2, '已注销')], default=1, verbose_name='状态'),
        ),
    ]
