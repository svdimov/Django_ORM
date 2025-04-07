from django.contrib import admin

from fruitipediaApp.fruits.models import Fruit, Category,Vegetables


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    pass

@admin.register(Vegetables)
class VegetablesAdmin(admin.ModelAdmin):
    pass
