# Generated by Django 5.1.2 on 2024-12-12 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shinku_1', '0011_alter_order_buyer_alter_order_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='good',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='good', to='shinku_1.goods', verbose_name='商品'),
        ),
    ]