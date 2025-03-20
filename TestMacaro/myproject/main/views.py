import os


import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

# Import your models here

from django.db.models import QuerySet, Avg
from datetime import datetime, timedelta, date

from main.models import Employee



def gender_replace()->None:
     Employee.objects.filter(gender='M').update(gender='Male')
     Employee.objects.filter(gender='F').update(gender='Female')


def salary_above()->None:
    salary_ab=Employee.objects.filter(salary__gte=9000).count()

    return salary_ab




