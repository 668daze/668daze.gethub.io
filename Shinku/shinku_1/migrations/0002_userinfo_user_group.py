# Generated by Django 5.1.2 on 2024-12-11 01:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shinku_1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='user_group',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, to='shinku_1.usergroup'),
        ),
    ]
