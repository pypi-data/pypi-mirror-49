# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-29 10:05
from __future__ import unicode_literals

import bpp.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bpp', '0105_rekord_z_konferencja'),
    ]

    operations = [
        migrations.AddField(
            model_name='uczelnia',
            name='pokazuj_ranking_autorow',
            field=bpp.models.fields.OpcjaWyswietlaniaField(choices=[('always', 'zawsze'), ('logged-in', 'tylko dla zalogowanych'), ('never', 'nigdy')], default='always', max_length=50, verbose_name='Pokazuj ranking autorów'),
        ),
        migrations.AddField(
            model_name='uczelnia',
            name='pokazuj_raport_autorow',
            field=bpp.models.fields.OpcjaWyswietlaniaField(choices=[('always', 'zawsze'), ('logged-in', 'tylko dla zalogowanych'), ('never', 'nigdy')], default='always', max_length=50, verbose_name='Pokazuj raport autorów'),
        ),
        migrations.AddField(
            model_name='uczelnia',
            name='pokazuj_raport_dla_komisji_centralnej',
            field=bpp.models.fields.OpcjaWyswietlaniaField(choices=[('always', 'zawsze'), ('logged-in', 'tylko dla zalogowanych'), ('never', 'nigdy')], default='always', max_length=50, verbose_name='Pokazuj raport dla Komisji Centralnej'),
        ),
        migrations.AddField(
            model_name='uczelnia',
            name='pokazuj_raport_jednostek',
            field=bpp.models.fields.OpcjaWyswietlaniaField(choices=[('always', 'zawsze'), ('logged-in', 'tylko dla zalogowanych'), ('never', 'nigdy')], default='always', max_length=50, verbose_name='Pokazuj ranking jednostek'),
        ),
        migrations.AddField(
            model_name='uczelnia',
            name='pokazuj_raport_wydzialow',
            field=bpp.models.fields.OpcjaWyswietlaniaField(choices=[('always', 'zawsze'), ('logged-in', 'tylko dla zalogowanych'), ('never', 'nigdy')], default='always', max_length=50, verbose_name='Pokazuj ranking wydziałów'),
        ),
        migrations.AlterField(
            model_name='uczelnia',
            name='pokazuj_status_korekty',
            field=bpp.models.fields.OpcjaWyswietlaniaField(choices=[('always', 'zawsze'), ('logged-in', 'tylko dla zalogowanych'), ('never', 'nigdy')], default='always', max_length=50, verbose_name='Pokazuj status korekty na stronie rekordu'),
        ),
    ]
