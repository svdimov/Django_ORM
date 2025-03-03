from django.contrib import admin
from django.contrib.auth.models import User

from main_app.models import Car




# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'year', 'owner', 'car_details']

    def car_details(self,obj:Car):

        try:
            owner_name = obj.owner.name
        except AttributeError:
            owner_name = 'No owner'


        try:
            registration_number = obj.registration.registration_number
        except AttributeError:
            registration_number = 'No registration number'

        return f"Owner: {owner_name}, Registration: {registration_number}"

    car_details.short_description = "Car Details"
