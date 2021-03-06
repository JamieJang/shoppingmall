# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 11:29
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('createAt', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-createAt'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.TextField()),
                ('photo', models.ImageField(blank=True, upload_to='shoppingmall/%Y/%m/%d')),
                ('price', models.PositiveIntegerField()),
                ('dcprice', models.PositiveIntegerField()),
                ('totalAmount', models.PositiveIntegerField()),
                ('detail', models.TextField(blank=True)),
                ('pubDate', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingmall.Category')),
            ],
            options={
                'ordering': ['category', '-pubDate'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="'-'를 제외하고 010xxxxxxxx 형식으로 입력해주세요", regex='^010\\d{4}\\d{4}$')])),
                ('homeAddress', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('createDate', models.DateField(auto_now_add=True)),
                ('cumulativeAmount', models.PositiveIntegerField()),
                ('level', models.PositiveIntegerField(default=1)),
                ('point', models.PositiveIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['level', '-createDate'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='shoppingmall.Tag'),
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoppingmall.Product'),
        ),
    ]
