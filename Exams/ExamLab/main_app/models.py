from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager


# Create your models here.

class Director(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    objects = DirectorManager()


class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50,default='Unknown')
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)



class Movie(models.Model):

    class GenreChoices(models.TextChoices):
        Action = 'Action','Action'
        Comedy = 'Comedy' ,'Comedy'
        Drama = 'Drama' , 'Drama'
        Other = 'Other' , 'Other'


    title = models.CharField(
    max_length=150,
    validators=[MinLengthValidator(5)]
    )
    release_date = models.DateField()
    storyline = models.TextField(null=True,blank=True)
    genre = models.CharField(
        max_length=6,
        choices=GenreChoices,
        default=GenreChoices.Other,


    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0
    )
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE,related_name='director_movies')
    starring_actor = models.ForeignKey(
        Actor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='starring_movies'

    )
    actors = models.ManyToManyField(Actor,related_name='actors_movies')









