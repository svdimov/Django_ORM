import os
from pprint import pprint
from tkinter.font import names

import django
from django.db import connection

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct, ProductManager
from django.db.models import Sum, Q, F


# print('All Products:')
# print(Product.objects.all())
# print()
# print('All Available Products:')
# print(Product.objects.available_products())
# print()
# print('All Available Food Products:')
# print(Product.objects.available_products_in_category("Food"))

# ===========================================================
#
def product_quantity_ordered()->str:
    orders = (Product.objects.annotate(total=Sum('orderproduct__quantity'))
              .exclude(total=None)
              .values('name', 'total')
              .order_by('-total'))

    return '\n'.join(f"Quantity ordered of {p['name']}: {p['total']}" for p in orders)




# def product_quantity_ordered()->str:
#     result = []
#     orders = (Product.objects.annotate(total=Sum('orderproduct__quantity'))
#               .exclude(total=None)
#               .values('name', 'total')
#               .order_by('-total'))
#     for order in orders:
#         result.append(f'Quantity ordered of {order["name"]}: {order["total"]}')
#
#     return '\n'.join(result)


def ordered_products_per_customer():
    orders = Order.objects.prefetch_related('orderproduct_set').order_by('id')
    result = []

    for order in orders:
        result.append(f"Order ID: {order.id}, Customer: {order.customer.username}")
        for product in order.orderproduct_set.all():
            result.append(f"- Product: {product.product.name}, Category: {product.product.category.name}")


    return '\n'.join(result)


def filter_products():
    products = Product.objects.filter(price__gt=3,is_available=True).order_by('-price', 'name')

    # products = Product.objects.filter(Q(price__gt=3) & Q(is_available=True)).order_by('-price', 'name')

    return '\n'.join(f"{p.name}: {p.price}lv."for p in products)


def give_discount():
    Product.objects.filter(is_available=True, price__gt=3.00).update(price=F('price') * 0.7)
    all_products = Product.objects.filter(is_available=True).order_by('-price', 'name')

    # reduction = F('price') *  0.7
    # query = Q(is_available=True) & Q(price__gt =3.00)
    # Product.objects.filter(query).update(price=reduction)
    # all_products = (Product.objects.filter(is_available=True)).order_by('-price', 'name')

    return '\n'.join(f"{p.name}: {p.price}lv." for p in all_products)



