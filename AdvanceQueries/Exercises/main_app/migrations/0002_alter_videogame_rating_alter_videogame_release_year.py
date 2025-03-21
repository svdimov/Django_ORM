# Generated by Django 5.0.4 on 2025-03-19 17:57

import main_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videogame',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2, validators=[main_app.validators.ValidRating(message='The rating must be between 0.0 and 10.0')]),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='release_year',
            field=models.PositiveIntegerField(validators=[main_app.validators.ValidReleaseYear(message='The release year must be between 1990 and 2023')]),
        ),
    ]
