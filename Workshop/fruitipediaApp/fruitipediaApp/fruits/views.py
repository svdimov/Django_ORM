from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from .models import Fruit, Category, Vegetables, Order

from .forms import CategoryForm, FruitAddForm, FruitEditForm, DeleteFruitForm, VegetablesEditForm, DeleteVegetablesForm, \
    VegetablesAddForm, OrderItemForm


# Create your views here.

@login_required
def index_view(request):
    query = request.GET.get('q', '')
    q_name = Q(name__icontains=query)
    q_id = Q(id__icontains=query)
    fruits = Fruit.objects.filter(q_name | q_id) if query else Fruit.objects.all()
    vegetables = Vegetables.objects.filter(q_name | q_id) if query else Vegetables.objects.all()

    context = {
        'query': query,
        'fruits': fruits,
        'vegetables': vegetables,
    }

    return render(request, 'common/index.html', context)
@login_required
def dashboard_view(request):
    query = request.GET.get('q', '')
    fruits = Fruit.objects.all()
    if query:
        # Filter fruits based on the search query
        q_name = Q(name__icontains=query)
        q_id = Q(id__icontains=query)
        fruits = fruits.filter(q_name | q_id)

    context = {'fruits': fruits,'query': query}

    return render(request, 'common/dashboard.html', context)

@login_required
def dashboard2_view(request):
    query = request.GET.get('q', '')
    vegetables = Vegetables.objects.all()
    if query:
        # Filter fruits based on the search query
        q_name = Q(name__icontains=query)
        q_id = Q(id__icontains=query)
        vegetables = vegetables.filter(q_name | q_id)

    context = {'vegetables': vegetables,'query': query }

    return render(request, 'common/dashboard2.html', context)

@login_required
def create_fruit_view(request):
    if request.method == 'GET':
        form = FruitAddForm()
    else:
        form = FruitAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'fruits/create-fruit.html', context)

@login_required
def fruit_details_view(request, pk):
    fruit = Fruit.objects.get(id=pk)
    context = {'fruit': fruit}
    return render(request, 'fruits/details-fruit.html', context)

@login_required
def edit_fruit_view(request, pk):
    fruit = Fruit.objects.get(id=pk)
    if request.method == 'GET':
        form = FruitEditForm(instance=fruit)
    else:
        form = FruitEditForm(request.POST, instance=fruit)
        if form.is_valid():
            fruit.save()
            return redirect('dashboard')


    context = {'form': form, 'fruit': fruit}
    return render(request, 'fruits/edit-fruit.html', context)

@login_required
def delete_fruit_view(request, pk):
    fruit = Fruit.objects.get(id=pk)
    if request.method == 'GET':
        form = DeleteFruitForm(instance=fruit)
    else:
        form = DeleteFruitForm(request.POST, instance=fruit)
        if form.is_valid():
            fruit.delete()
            return redirect('dashboard')

    context = {'form': form, 'fruit': fruit}

    return render(request, 'fruits/delete-fruit.html', context)

@login_required
def create_category_view(request):
    if request.method == 'GET':
        form = CategoryForm()
    else:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}


    return render(request, 'categories/create-category.html', context)

#create Vegetables
@login_required
def create_vegetables_view(request):
    if request.method == 'GET':
        form = VegetablesAddForm()
    else:
        form = VegetablesAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard2')

    context = {'form': form}

    return render(request, 'vegetables/create-vegetables.html', context)

@login_required
def vegetables_details_view(request, pk):
    vegetables = Vegetables.objects.get(id=pk)
    context = {'vegetables': vegetables}
    return render(request, 'vegetables/details-vegetables.html', context)

@login_required
def edit_vegetables_view(request, pk):
    vegetable = Vegetables.objects.get(id=pk)
    if request.method == 'GET':
        form = VegetablesEditForm(instance=vegetable)
    else:
        form = VegetablesEditForm(request.POST, instance=vegetable)
        if form.is_valid():
            vegetable.save()
            return redirect('dashboard2')


    context = {'form': form, 'vegetable': vegetable}
    return render(request, 'vegetables/edit-vegetables.html', context)

@login_required
def delete_vegetables_view(request, pk):
    vegetable = Vegetables.objects.get(id=pk)
    if request.method == 'GET':
        form = DeleteVegetablesForm(instance=vegetable)
    else:
        form = DeleteVegetablesForm(request.POST, instance=vegetable)
        if form.is_valid():
            vegetable.delete()
            return redirect('dashboard2')

    context = {'form': form, 'vegetable': vegetable}

    return render(request, 'vegetables/delete-vegetables.html', context)

# views.py

def create_fruit_order(request, pk):
    # Fetch the fruit that the user wants to order
    fruit = get_object_or_404(Fruit, pk=pk)


    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            # Create a new Order
            order = Order.objects.create()  # Create an order without passing fruit or quantity here
            # Now create the order item and associate it with the order
            order_item = form.save(commit=False)
            order_item.order = order  # Set the order relationship
            order_item.fruit = fruit  # Set the fruit for this order item

            order_item.save()

            # Redirect to the success page or wherever you need to go
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderItemForm()

    return render(request, 'orders/create_order.html', {'form': form, 'fruit': fruit})

def create_vegetable_order(request, pk):
    vegetable = get_object_or_404(Vegetables, pk=pk)

    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = Order.objects.create()
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.vegetable = vegetable
            order_item.save()

            return redirect('order_success', order_id=order.id)
    else:
        form = OrderItemForm()

    return render(request, 'orders/create_vegetable_order.html', {'form': form, 'vegetable': vegetable})


@login_required
def order_success(request, order_id):

    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    # Pass the order to the template
    return render(request, 'orders/order_success.html', {'order': order})
