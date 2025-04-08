from django.core.validators import MinLengthValidator
from django.db import models
from .validators import  only_letters_validator

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Fruit(models.Model):
    class Meta:
        permissions = [
            ("can_add_fruit", "Can add fruit"),
            ("can_delete_fruit", "Can delete fruit"),
        ]

    name = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
            only_letters_validator
        ]

    )
    image_url = models.URLField()
    description = models.TextField()
    nutrition = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='fruits',
        null=True,
        blank=True
    )

class Vegetables(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
            only_letters_validator
        ]

    )
    image_url = models.URLField()
    description = models.TextField()
    nutrition = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='Vegetables',
        null=True,
        blank=True
    )

