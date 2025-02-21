from django.db import models

class StatusChoices(models.TextChoices):
    PENDING = 'Pen', 'Pending'
    Completed = 'Comp', 'Completed'
    Cancelled = 'Can', 'Cancelled'
