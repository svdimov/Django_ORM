from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import PublisherManager
from main_app.mixins import MixinRating,MixinUpdate


# Create your models here.
#Optimization Models

class Publisher(MixinRating):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )
    established_date = models.DateField(default='1800-01-01')
    country = models.CharField(max_length=100, default='TBC')

    objects = PublisherManager()


class Author(MixinUpdate):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=40, default='TBC')
    is_active = models.BooleanField(default=True)



class Book(MixinRating,MixinUpdate):
    class GenreChoice(models.TextChoices):
        Fiction = 'Fiction', 'Fiction'
        Non_Fiction = 'Non-Fiction', 'Non-Fiction'
        Other = 'Other', 'Other'

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)]
    )
    publication_date = models.DateField()
    summary = models.TextField(null=True, blank=True)
    genre = models.CharField(
        max_length=11,
        choices=GenreChoice,
        default=GenreChoice.Other
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        validators=[MinValueValidator(0.01), MaxValueValidator(6.0)],
        default=0.01
    )

    is_bestseller = models.BooleanField(default=False)


    publisher = models.ForeignKey(
        Publisher,on_delete=models.CASCADE,
        related_name='books_publisher',
    )
    main_author = models.ForeignKey(
        Author,on_delete=models.CASCADE,
        related_name='books_author',
    )
    co_authors = models.ManyToManyField(Author, related_name='books_co_authors')





















