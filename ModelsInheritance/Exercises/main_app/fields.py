from django.core.exceptions import ValidationError
from django.db import models


class StudentIDField(models.PositiveIntegerField):

    @staticmethod
    def validate_field(value) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError('Invalid input for student ID')

    def to_python(self, value) -> int:
        return self.validate_field(value)

    def get_prep_value(self, value) -> int:
        validate_field = self.validate_field(value)

        if validate_field <= 0:
            raise ValidationError("ID cannot be less than or equal 	to zero")
        return validate_field


# ===========================================
# class MaskedCreditCardField(models.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs['max_length'] = 20
#         super().__init__(*args, **kwargs)
#
#     def to_python(self, value):
#
#         if not isinstance(value, str):
#             raise ValidationError("The card number must be a string")
#         if not value.isdigit():
#             raise ValidationError("The card number must contain only digits")
#         if len(value) != 16:
#             raise ValidationError("The card number must be exactly 16 characters long")
#
#         return f"****-****-****-{value[-4:]}"

from django.db import models
from django.core.exceptions import ValidationError


def mask_card_number(value):
    """Mask the credit card number."""
    return f"****-****-****-{value[-4:]}"


class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20  # Set max length
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """Prepare value before saving to the database."""
        if value is None:
            return value
        return mask_card_number(value)

    def to_python(self, value):
        """Convert the value to Python type and validate."""
        if value is None:
            return value
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")
        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")
        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")
        return mask_card_number(value)




