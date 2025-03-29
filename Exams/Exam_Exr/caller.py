import os
from statistics import quantiles

import django
from django.db import connection, transaction

from django.db.models import Count, Q, F, Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order


# Create queries within functions


# Create Profiles

def get_profiles(search_string=None) -> str:
    query = (Q(full_name__icontains=search_string)
             | Q(email__icontains=search_string)
             | Q(phone_number__icontains=search_string))

    if search_string is None:
        return ''
    profiles = Profile.objects.filter(query).order_by('full_name')

    return '\n'.join(f'Profile: '
                     f'{p.full_name}, email: '
                     f'{p.email}, phone number:'
                     f' {p.phone_number}, orders: '
                     f'{p.orders_profiles.count()}' for p in profiles)


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles:  # Correct check for an empty QuerySet
        return ''

    return '\n'.join(
        f"Profile: {p.full_name}, orders: {p.orders_profiles.count()}"
        for p in profiles
    )


def get_last_sold_products():
    last_product = Order.objects.prefetch_related('products').last()

    if last_product is None or last_product.products.count() == 0:
        return ''

    product_name = ', '.join(p.name for p in last_product.products.all())
    return f"Last sold products: {product_name}"


# ==================================================

def get_top_products():
    top_product = Product.objects.annotate(product_count=Count('orders_products')).filter(product_count__gt=0) \
                      .order_by('-product_count', 'name')[:5]

    if not top_product.exists():
        return ''

    return "Top products:\n" + '\n'.join(f"{p.name}, sold {p.product_count} times" for p in top_product)


def apply_discounts():
    orders = ((Order.objects.
               annotate(product_count=Count('products'))
               .filter(product_count__gt=2, is_completed=False)
               .update(total_price=F('total_price') * 0.9))
    )

    return f"Discount applied to {orders} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if order is None:
        return ''
    Product.objects.filter(orders_products=order).update(in_stock=F('in_stock') - 1, is_available=Case(
        When(in_stock=1, then=Value(False)),
        default=F('is_available')
    ))


    order.is_completed = True
    order.save()
    return "Order has been completed!"

# def complete_order():
#     order = Order.objects.filter(is_completed=False).order_by('creation_date').select_related('profile').prefetch_related('products').first()
#
#     if not order:
#         return 'No pending orders.'
#
#     with transaction.atomic():  # Ensures database integrity
#         for product in order.products.all():
#             if product.in_stock <= 0:  # Check stock before updating
#                 return f"Cannot complete order. Product '{product.name}' is out of stock."
#
#             product.in_stock -= 1
#             if product.in_stock == 0:
#                 product.is_available = False
#             product.save()
#
#         order.is_completed = True
#         order.save()
#
#     return "Order has been successfully completed!"


print(complete_order())
print(len(connection.queries))