# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 07:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingmall', '0022_remove_purchase_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='purchageNumber',
            new_name='purchaseNumber',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='purchageNumber',
            new_name='purchaseNumber',
        ),
    ]