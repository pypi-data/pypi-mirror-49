# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-04 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_account', '0004_delete_chatconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='OPClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuer', models.URLField()),
                ('client_id', models.CharField(max_length=255)),
            ],
        ),
    ]
