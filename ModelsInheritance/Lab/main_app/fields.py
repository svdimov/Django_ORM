from main_app import models
from django.db import models


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = (
            (True, 'Available'),
            (False, 'Not Available')
        )
        kwargs['default'] = True
        super().__init__(*args, **kwargs)


from django.db import models
from django.core.exceptions import ValidationError

from datetime import date

class DateRangeField(models.Field):
    description = "A field to store date ranges"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'varchar(255)'  # Store the range as a string (ISO format)

    def get_prep_value(self, value):
        if value:
            start_date, end_date = value
            # Ensure that start_date and end_date are date objects before calling isoformat()
            if isinstance(start_date, str):
                start_date = date.fromisoformat(start_date)  # Convert string to date object
            if isinstance(end_date, str):
                end_date = date.fromisoformat(end_date)  # Convert string to date object

            return f'{start_date.isoformat()} to {end_date.isoformat()}'
        return None

    def from_db_value(self, value, expression, connection, context):
        if value:
            start_date_str, end_date_str = value.split(' to ')
            return (start_date_str, end_date_str)
        return None

