# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-19 20:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bpp', '0093_konferencja_wydawnictwo_ciagle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seria_Wydawnicza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=512, unique=True)),
                ('issn', models.CharField(blank=True, max_length=32, null=True, verbose_name='ISSN')),
                ('e_issn', models.CharField(blank=True, max_length=32, null=True, verbose_name='e-ISSN')),
            ],
            options={
                'ordering': ['nazwa'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='wydawnictwo_zwarte',
            name='numer_w_serii',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wydawnictwo_zwarte',
            name='seria_wydawnicza',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bpp.Seria_Wydawnicza'),
        ),
    ]
