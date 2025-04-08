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

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match!")
#         return cleaned_data