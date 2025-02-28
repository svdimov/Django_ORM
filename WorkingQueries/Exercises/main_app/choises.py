from django.db import models


class LaptopBrand(models.TextChoices):
    Asus = 'Asus', 'Asus'
    Acer = 'Acer', 'Acer'
    Apple = 'Apple', 'Apple'
    Lenovo = 'Lenovo', 'Lenovo'
    Dell = 'Dell', 'Dell'


class OperationSystemType(models.TextChoices):
    Windows = 'Windows', 'Windows'
    MacOS = 'MacOS', 'MacOS'
    Linux = 'Linux', 'Linux'
    Chrome_OS = 'Chrome OS', 'Chrome OS'


class DifficultyChoices(models.TextChoices):
    Easy = 'Easy', 'Easy'
    Medium = 'Medium', 'Medium'
    Hard = 'Hard', 'Hard'


class WorkoutTypeChoices(models.TextChoices):
    Cardio = 'Cardio', 'Cardio'
    Strength = 'Strength', 'Strength'
    Yoga = 'Yoga', 'Yoga'
    CrossFit = 'CrossFit', 'CrossFit'
    Calisthenics = 'Calisthenics', 'Calisthenics'
