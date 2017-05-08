# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-08 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VariantDatabase', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='varianttranscript',
            name='CDS_position',
        ),
        migrations.AddField(
            model_name='variant',
            name='sample_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]