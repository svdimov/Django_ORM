from django.db import models
from datetime import date

class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField(default=False)  # Fixed default issue
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):

    class Cities(models.TextChoices):
        Sofia = 'Sofia', 'Sofia'
        Plovdiv = 'Plovdiv', 'Plovdiv'
        Burgas = 'Burgas', 'Burgas'
        Varna = 'Varna', 'Varna'

    code = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.PositiveIntegerField(default=1, verbose_name='Employees Count')
    location = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=Cities.choices
    )
    last_edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_in_days = models.PositiveIntegerField(null=True, blank=True, verbose_name='Duration in Days')
    estimated_hours = models.FloatField(null=True, blank=True, verbose_name='Estimated Hours')
    start_date = models.DateField(default=date.today, verbose_name='Start Date')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name
