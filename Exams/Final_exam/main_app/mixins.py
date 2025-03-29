from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MixinRating(models.Model):
    class Meta:
        abstract = True


    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
class MixinUpdate(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)