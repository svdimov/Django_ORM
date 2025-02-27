import os
import django
from datetime import date
from django.db import connection, reset_queries

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student
from django.db import connection, reset_queries


# Run and print your queries

def add_students():
    Student.objects.bulk_create([
        Student(
            student_id='FC5204',
            first_name='John',
            last_name='Doe',
            birth_date='1995-05-15',
            email='john.doe@university.com'
        ),
        Student(
            student_id='FE0054',
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@university.com'
        ),
        Student(
            student_id='FH2014',
            first_name='Alice',
            last_name='Johnson',
            birth_date='1998-02-10',
            email='alice.johnson@university.com'
        ),
        Student(
            student_id='FH2015',
            first_name='Bob',
            last_name='Wilson',
            birth_date='1996-11-25',
            email='bob.wilson@university.com'
        )
    ])

# select
def get_students_info():
    all_students = Student.objects.all()

    return '\n'.join(f'Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}' for s in all_students)


#update
def update_students_emails():
    students_email = Student.objects.all()
    for s in students_email:
        s.email = s.email.replace(s.email.split('@')[1], 'uni-students.com')
        s.save()

#delete
def truncate_students():
    Student.objects.all().delete()

print(connection.queries)