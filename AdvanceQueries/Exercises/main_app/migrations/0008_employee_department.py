# Generated by Django 5.0.4 on 2025-03-19 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_remove_employee_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
