import re

from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


# def validate_menu_categories(value):
#
#     categories = ["Appetizers", "Main Course", "Desserts"]
#
#     for category in categories:
#         if value not in category:
#             raise ValidationError(
#                 'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')
#
#

def validate_name(value:str):
    if not value.isalpha() and  not value.strip():
        raise ValidationError('Name can only contain letters and spaces')


# def valid_age(value:int):
#     if value < 18:
#         raise ValidationError('Age must be greater than or equal to 18')
#
#
# def validate_phone_number(value:str):
#     if not value.startswith('+359') and  not len(value)  > 12:
#         raise ValidationError('Phone number must start with "+359" followed by 9 digits')
@deconstructible
class ValidateName:
    def __init__(self, message):
        self.message = message
    def __call__(self, value):
        for char in value:
            if not (char.isalpha() or char.isspace()):
                raise ValidationError(self.message)
@deconstructible
class ValidatePhoneNumber:
    def __init__(self, message:str):
        self.message = message
    def __call__(self, value):
        if not re.match(r'^\+359\d{9}$', value):
            raise ValidationError(self.message)

        # if not value.startswith('+359') or len(value) != 13:
        #     raise ValidationError(self.message)