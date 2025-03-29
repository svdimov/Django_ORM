# Generated by Django 5.0.4 on 2025-03-29 07:26

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3)])),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('country', models.CharField(default='TBC', max_length=40)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3)])),
                ('established_date', models.DateField(default='1800-01-01')),
                ('country', models.CharField(default='TBC', max_length=100)),
                ('rating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2)])),
                ('publication_date', models.DateField()),
                ('summary', models.TextField(blank=True, null=True)),
                ('genre', models.CharField(choices=[('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('Other', 'Other')], default='Other', max_length=11)),
                ('price', models.DecimalField(decimal_places=2, default=0.01, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(6.0)])),
                ('rating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('is_bestseller', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('co_authors', models.ManyToManyField(related_name='books_co_authors', to='main_app.author')),
                ('main_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_author', to='main_app.author')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_publisher', to='main_app.publisher')),
            ],
        ),
    ]
