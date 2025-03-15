from django.contrib import admin
from django.contrib.auth.models import User

from main_app.models import MenuReview, Restaurant, Menu


# Register your models here.
@admin.register(MenuReview)
class MenuReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass

