# Generated by Django 5.0.4 on 2025-03-15 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_userprofile_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='id_read',
            new_name='is_read',
        ),
    ]
