from django.contrib import admin
from main_app.models import Person,Blog,WeatherForecast,Recipe,Book

# Register your models here.
admin.site.register(Person)
admin.site.register(Blog)
admin.site.register(WeatherForecast)
admin.site.register(Recipe)
admin.site.register(Book)