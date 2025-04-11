from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
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
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='fruits',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name

class Vegetables(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
            only_letters_validator
        ]

    )
    image_url = models.URLField()
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='Vegetables',
        null=True,
        blank=True
    )

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    fruit = models.ForeignKey(Fruit, null=True, blank=True, on_delete=models.CASCADE)
    vegetable = models.ForeignKey(Vegetables, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=10,validators=[MinValueValidator(0.01)]) # it is kilograms

