# Generated by Django 5.1.5 on 2025-02-16 01:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0002_alter_checklist_table'),
        ('medical_records', '0002_alter_medicalrecord_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_records.medicalrecord'),
        ),
    ]
