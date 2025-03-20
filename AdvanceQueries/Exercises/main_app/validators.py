from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidRating:
    def __init__(self,message):
        self.message = message

    def __call__(self, value):
        if value < 0.0 or value > 10:
            raise ValidationError(self.message)


@deconstructible
class ValidReleaseYear:
    def __init__(self,message):
        self.message = message
    def __call__(self, value):
        if value < 1999 or value > 2023:
            raise ValidationError(self.message)