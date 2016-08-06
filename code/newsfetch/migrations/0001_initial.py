# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-05 14:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_desc', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Fetcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fetcher_name', models.CharField(max_length=200)),
                ('fetcher_desc', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newscategory', models.CharField(max_length=200)),
                ('content_snippet', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=400)),
                ('source', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('md5hash', models.CharField(max_length=200)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_text', models.CharField(max_length=200)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsfetch.Category')),
            ],
        ),
        migrations.AddField(
            model_name='newsitem',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsfetch.Topic'),
        ),
        migrations.AddField(
            model_name='category',
            name='fetcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsfetch.Fetcher'),
        ),
    ]
