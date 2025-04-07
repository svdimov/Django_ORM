from django import forms
from django.contrib.auth.views import LoginView

from .models import Category, Fruit, Vegetables


class CategoryBaseForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class FruitBaseForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = '__all__'

class VegetablesBaseForm(forms.ModelForm):
    class Meta:
        model = Vegetables
        fields = '__all__'


class CategoryForm(CategoryBaseForm):
    pass

#Fruits
class FruitAddForm(FruitBaseForm):
    pass


class FruitEditForm(FruitBaseForm):
    pass

class DeleteFruitForm(FruitBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


#Vegetables
class VegetablesAddForm(VegetablesBaseForm):
    pass


class VegetablesEditForm(VegetablesBaseForm):
    pass


class DeleteVegetablesForm(VegetablesBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True

