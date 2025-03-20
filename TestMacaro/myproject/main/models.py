from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # Assuming salary is a number

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.salary}"