from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models

from main_app.managers import ProfileManager


# Create your models here.

class CreationDateMixin(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)



class Profile(CreationDateMixin):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)])
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    objects = ProfileManager()


class Product(CreationDateMixin):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        validators=[MinValueValidator(0.01)]
    )
    in_stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)


class Order(CreationDateMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        validators=[MinValueValidator(0.01)]
    )
    is_completed = models.BooleanField(default=False)



