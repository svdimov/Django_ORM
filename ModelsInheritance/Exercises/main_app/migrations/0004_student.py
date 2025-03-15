# Generated by Django 5.0.4 on 2025-03-15 09:38

import main_app.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_rename_id_read_message_is_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('student_id', main_app.fields.StudentIDField()),
            ],
        ),
    ]
