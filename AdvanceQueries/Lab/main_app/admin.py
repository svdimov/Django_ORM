from django.contrib import admin
from django.contrib.auth.models import User

from main_app.models import Category, Product, Customer, Order, OrderProduct


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass

