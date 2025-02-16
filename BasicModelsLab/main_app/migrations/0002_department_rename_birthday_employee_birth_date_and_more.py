# Generated by Django 5.0.4 on 2025-02-15 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('employees_count', models.IntegerField(default=1, verbose_name='Employees Count')),
                ('location', models.CharField(blank=True, choices=[('Sofia', 'Sofia'), ('Plovdiv', 'Plovdiv'), ('Burgas', 'Burgas'), ('Varna', 'Varna')], max_length=20, null=True)),
                ('last_edited_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='birthday',
            new_name='birth_date',
        ),
        migrations.AddField(
            model_name='employee',
            name='photo',
            field=models.URLField(default='2025-02-15'),
            preserve_default=False,
        ),
    ]
