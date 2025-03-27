import datetime

from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models

from main_app.managers import HouseManager


# Create your models here.


class BaseMixin(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5), MaxLengthValidator(80)],
        unique=True,
    )
    modified_at = models.DateTimeField(auto_now=True)
    wins = models.PositiveSmallIntegerField(default=0)


class House(BaseMixin):
    # name = models.CharField(
    #     max_length=80,
    #     validators=[MinLengthValidator(5), MaxLengthValidator(80)],
    #     unique=True,
    # )
    motto = models.TextField(null=True, blank=True)
    is_ruling = models.BooleanField(default=False)
    castle = models.CharField(
        max_length=80,
        validators=[MaxLengthValidator(80)],
        null=True,
        blank=True,
    )
    # wins = models.PositiveSmallIntegerField(default=0)
    # modified_at = models.DateTimeField(auto_now=True)


    objects = HouseManager()



class Dragon(BaseMixin):


    class BreathChoice(models.TextChoices):
        Fire = "Fire",'Fire'
        Ice = "Ice",'Ice'
        Lightning = "Lightning",'Lightning'
        Unknown = "Unknown",'Unknown'



    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        default=1.0
    )
    breath = models.CharField(
        max_length=9,
        validators=[MaxLengthValidator(9)],
        choices=BreathChoice,
        default=BreathChoice.Unknown)

    is_healthy = models.BooleanField(default=True)
    birth_date = models.DateField(default=datetime.date.today)
    house = models.ForeignKey(House, on_delete=models.CASCADE,related_name='dragons_houses')


class Quest(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5), MaxLengthValidator(80)],
        unique=True,
    )
    code = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(regex=r'^[A-Za-z#]{4}$')],
        unique=True,
    )
    reward = models.FloatField(default=100.0)
    start_time = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True)

    dragons = models.ManyToManyField(Dragon,related_name='quests_dragons')
    host = models.ForeignKey(House, on_delete=models.CASCADE,related_name='quests_houses')






