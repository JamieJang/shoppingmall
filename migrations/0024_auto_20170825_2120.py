# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 12:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingmall', '0023_auto_20170825_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='totalPrice',
            new_name='total_price',
        ),
    ]