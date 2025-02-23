# Generated by Django 5.1.6 on 2025-02-21 08:34

from django.db import migrations
from django.db.models import F, Case, When, Value, CharField
MULTIPLIER = 120

def update_price(apps, schema_editor):
    current_price = apps.get_model('main_app', 'SmartPhone')
    current_price.objects.update(price=F('price') * MULTIPLIER)

def update_category(apps, schema_editor):
    current_category = apps.get_model('main_app', 'SmartPhone')
    current_category.objects.update(category=Case(
        When(price__gte=750, then=Value('Expensive')),
        default=Value('Cheap'),
        output_field=CharField(),
    ))

def revers_price(apps, schema_editor):
    current_price = apps.get_model('main_app', 'SmartPhone')
    current_price.objects.update(price = F('price') / MULTIPLIER)

def revers_category(apps, schema_editor):
    current_category = apps.get_model('main_app', 'SmartPhone')
    default_category = current_category._meta.get_field('category').default
    current_category.objects.update(category= default_category)

def update_price_category(apps, schema_editor):
    update_price(apps, schema_editor)
    update_category(apps, schema_editor)

def revers_price_category(apps, schema_editor):
    revers_price(apps, schema_editor)
    revers_category(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_smartphone'),
    ]

    operations = [migrations.RunPython(update_price_category, reverse_code=revers_price_category)]

