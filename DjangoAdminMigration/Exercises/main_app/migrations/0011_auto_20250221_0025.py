# Generated by Django 5.1.6 on 2025-02-20 22:25

from django.db import migrations
# The bad way
# def age_groped(apps, schema_editor):
#     current_person = apps.get_model('main_app', 'Person')
#     people = current_person.objects.all()
#     for person in people:
#         if person.age <= 12:
#             person.age_group = 'Child'
#         elif 13 <=person.age < 17:
#             person.age_group = 'Teen'
#         else:
#             person.age_group = 'Adult'
#
#         person.save()
#
# def reverse_age_groped(apps, schema_editor):
#     current_person = apps.get_model('main_app', 'Person')
#     default_person = current_person._meta.get_field('age_group').default
#
#     for person in current_person.objects.all():
#         person.age_group = default_person
#         person.save()
from django.db.models import Case, When, Value, CharField

# The right way
def age_grouped(apps, schema_editor):
    Person = apps.get_model('main_app', 'Person')

    # Efficient bulk update using Case and When
    Person.objects.update(
        age_group=Case(
            When(age__lte=12, then=Value('Child')),
            When(age__gte=13, age__lte=17, then=Value('Teen')),
            When(age__gte=18, then=Value('Adult')),
            default=Value('Unknown'),  # In case age is NULL or not set
            output_field=CharField(),
        )
    )

def reverse_age_grouped(apps, schema_editor):
    Person = apps.get_model('main_app', 'Person')
    default_value = Person._meta.get_field('age_group').default or ''  # Handle if no default

    # Efficiently reset all age_group values
    Person.objects.update(age_group=default_value)


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_person'),
    ]

    operations = [migrations.RunPython(age_grouped, reverse_code=reverse_age_grouped)]

