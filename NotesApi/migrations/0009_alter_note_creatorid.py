# Generated by Django 3.2.24 on 2024-02-20 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NotesApi', '0008_alter_note_creatorid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='creatorId',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
