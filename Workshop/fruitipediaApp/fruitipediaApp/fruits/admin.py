from django.contrib import admin
from fruitipediaApp.fruits.models import Fruit, Category, Vegetables

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):

    # Prevent deleting items
    def has_delete_permission(self, request, obj=None):
        return False  # Always deny delete

    # Prevent adding new items
    def has_add_permission(self, request):
        return False  # Prevent adding items

    # Allow changing but not adding or deleting
    def has_change_permission(self, request, obj=None):
        return True  # Allow changing but not adding or deleting

@admin.register(Vegetables)
class VegetablesAdmin(admin.ModelAdmin):
    pass
