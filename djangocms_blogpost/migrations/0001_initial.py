# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 08:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djangocms_blogpost.models
import djangocms_text_ckeditor.fields
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0004_auto_20160328_1434'),
        ('cms', '0014_auto_20160404_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=100)),
                ('body', djangocms_text_ckeditor.fields.HTMLField(verbose_name='Text')),
                ('image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, to='filer.Image', verbose_name='Bild')),
            ],
            options={
                'abstract': False,
            },
            bases=(djangocms_blogpost.models.CreatePageMixin, 'cms.cmsplugin'),
        ),
    ]
