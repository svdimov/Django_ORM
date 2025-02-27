from django.db import models

class RoomTypeChoices(models.TextChoices):
    Standard = 'Standard','Standard'
    Deluxe = 'Deluxe','Deluxe'
    Suite = 'Suite','Suite'

class CharacterTypeChoices(models.TextChoices):
    Mage = 'Mage','Mage'
    Warrior = 'Warrior','Warrior'
    Assassin = 'Assassin','Assassin'
    Scout = 'Scout','Scout'
    Fusion = 'Fusion','Fusion'
