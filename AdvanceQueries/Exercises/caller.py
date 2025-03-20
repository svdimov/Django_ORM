import os
from datetime import date
from itertools import count
from tkinter.font import names

import django
from django.db import connection
from django.db.models import Q, F, Count, Avg, Sum, Case, When, Value, CharField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Task, Exercise, Employee
#
# Employee.objects.update(department=Case(
#     When (salary__range=(0,2000), then=Value('cleaner')),
#     When (salary__range=(2000,4000), then=Value('Human Resources')),
#     When (salary__range=(4000,7000), then=Value('IT')),
#     When (salary__range=(7000,10000), then=Value('Directors')),
#     default=Value('Unassigned'),
#     output_field=CharField(),
#
#
# ))

EM = Employee.objects.filter(salary__range=(1500,4500))
for e in EM:
    print(e)