# Generated by Django 3.2.24 on 2024-02-21 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NotesApi', '0013_alter_note_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versionhistory',
            name='editorId',
            field=models.UUIDField(),
        ),
    ]
