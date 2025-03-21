import os
import django
from django.db import connection
from django.db.models import Count, Q, F, Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order

# Create queries within functions



# Create Profiles

def get_profiles(search_string=None)->str:
    query =(Q(full_name__icontains=search_string)
            | Q(email__icontains=search_string)
            | Q(phone_number__icontains=search_string))

    if search_string is None:
        return ''
    profiles = Profile.objects.filter(query).order_by('full_name')

    return '\n'.join(f'Profile: '
                     f'{p.full_name}, email: '
                     f'{p.email}, phone number:'
                     f' {p.phone_number}, orders: '
                     f'{p.order_set.count()}'for p in profiles)


def get_loyal_profiles()->str:
    profiles = Profile.objects.get_regular_customers()

    if profiles is None:
        return ''

    return '\n'.join(f""
                     f"Profile: {p.full_name}, "
                     f"orders: {p.order_count}"
                     for p in profiles)

def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ""

    product_name = [p.name for p in last_order.products.all()]

    return f"Last sold products: {', '.join(product_name)}"



def get_top_products():
    top_products = Product.objects\
                       .annotate(count_product=Count('order'))\
                       .filter(count_product__gt=0)\
                       .order_by( '-count_product', 'name')[:5]

    if not top_products.exists():
        return ''

    return "Top products:\n" + '\n'.join(f"{p.name}, sold {p.count_product} times" for p in top_products)


def apply_discounts():

    discount = Order.objects\
        .annotate(count_product=Count('products'))\
        .filter(is_completed=False, count_product__gt=2)\
        .update(total_price=F('total_price') * 0.9)




    return f"Discount applied to {discount} orders."


def complete_order():
    order = Order.objects\
        .filter(is_completed=False)\
        .order_by('creation_date').first()
    if order is None:
        return ''

    Product.objects.filter(order=order)\
        .update(in_stock=F('in_stock') - 1, is_available=Case(
        When(in_stock=1, then=Value(False)),
        default=F('is_available')
    ))

    order.is_completed = True
    order.save()

    return "Order has been completed!"




print(len(connection.queries))



