# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-30 22:29
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180501_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carhistory',
            name='service',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', 'PanelBeating'), ('2', 'ElectricalWiring'), ('3', 'Engine'), ('4', 'Painting'), ('5', 'GeneralMaintenance')], max_length=9),
        ),
    ]
