# Generated by Django 5.1.5 on 2025-02-16 01:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist_items', '0002_alter_checklistitem_table'),
        ('checklists', '0002_alter_checklist_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistitem',
            name='checklist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklistItems', to='checklists.checklist'),
        ),
    ]
