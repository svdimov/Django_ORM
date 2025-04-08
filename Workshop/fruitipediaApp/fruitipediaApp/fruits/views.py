from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from django.shortcuts import render, redirect
from .models import Fruit, Category,Vegetables

from .forms import CategoryForm, FruitAddForm, FruitEditForm, DeleteFruitForm, VegetablesEditForm, DeleteVegetablesForm, \
    VegetablesAddForm


# Create your views here.

@login_required
def index_view(request):
    return render(request, 'common/index.html')

@login_required
def dashboard_view(request):
    query = request.GET.get('q', '')
    fruits = Fruit.objects.all()
    if query:
        # Filter fruits based on the search query
        fruits = fruits.filter(name__icontains=query)

    context = {'fruits': fruits,'query': query}

    return render(request, 'common/dashboard.html', context)

@login_required
def dashboard2_view(request):
    query = request.GET.get('q', '')
    vegetables = Vegetables.objects.all()
    if query:
        # Filter fruits based on the search query
        vegetables = vegetables.filter(name__icontains=query)

    context = {'vegetables': vegetables,'query': query }

    return render(request, 'common/dashbord2.html', context)

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








