# Generated by Django 3.2.24 on 2024-02-20 19:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('NotesApi', '0009_alter_note_creatorid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='history',
        ),
        migrations.RemoveField(
            model_name='versionhistory',
            name='versionNumber',
        ),
        migrations.AddField(
            model_name='note',
            name='historyIds',
            field=models.TextField(default='[]'),
        ),
        migrations.AlterField(
            model_name='versionhistory',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
