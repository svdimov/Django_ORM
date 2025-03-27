from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator, MinLengthValidator
from django.db import models
from django.db.models import SET_NULL

from main_app.managers import TennisPlayerManager


# Create your models here.
class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(5),MaxLengthValidator(120)]
    )
    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    ranking = models.PositiveIntegerField(
        validators=[MaxValueValidator(300),MinValueValidator(1)]
    )
    is_active = models.BooleanField(default=True)

    objects = TennisPlayerManager()



class Tournament(models.Model):

    class SurfaceChoice(models.TextChoices):
        Not_Selected = 'Not Selected', 'Not Selected'
        Clay = 'Clay', 'Clay'
        Grass = 'Grass', 'Grass'
        Hard_Court = 'Hard Court', 'Hard Court'


    name = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(2),MaxLengthValidator(150)],
        unique=True
    )
    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    start_date = models.DateField()
    surface_type = models.CharField(
        max_length=12,
        choices=SurfaceChoice,
        default=SurfaceChoice.Not_Selected,
    )



class Match(models.Model):

    class Meta:
        verbose_name_plural = 'Matches'

    score = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)]
    )
    summary = models.TextField(
        validators=[MinLengthValidator(5)]
    )
    date_played = models.DateTimeField()

    tournament = models.ForeignKey(Tournament,
                                   on_delete=models.CASCADE,
                                   related_name='matches_tournament'
                                   )
    players = models.ManyToManyField(
        TennisPlayer,
        related_name='matches_players')
    winner = models.ForeignKey(TennisPlayer,
                               on_delete=models.SET_NULL,
                               related_name='matches_winner',
                               null=True
                               )

