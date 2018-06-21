# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-12 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20180612_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mileage', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('regular_maintenance', models.TextField(help_text='update on regular maintenance', max_length=1000)),
                ('replace_part', models.TextField(help_text='part replaced', max_length=500)),
                ('repair_type', models.TextField(help_text='type of repair done', max_length=1000)),
                ('mechanic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.MechProfile')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Vehicle')),
            ],
        ),
    ]