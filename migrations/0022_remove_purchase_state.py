# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 07:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingmall', '0021_auto_20170825_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='state',
        ),
    ]
