from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from . import views
from .views import (
    index_view, dashboard_view, create_fruit_view,
    fruit_details_view, edit_fruit_view, delete_fruit_view,
    create_category_view, create_vegetables_view,
    vegetables_details_view, edit_vegetables_view,
    delete_vegetables_view, dashboard2_view,
)

urlpatterns = [
    path('', index_view, name='index'),

    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', LoginView.as_view(template_name='auth/login.html'), name='home'),  # First page = login

    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard2/', dashboard2_view, name='dashboard2'),
    path('create-fruit/', create_fruit_view, name='create_fruit'),

    path('<int:pk>/', include([
        path('fruit-detail/', fruit_details_view, name='fruit_detail'),
        path('edit-fruit/', edit_fruit_view, name='edit_fruit'),
        path('delete-fruit/', delete_fruit_view, name='delete_fruit'),
    ])),

    path('create-category/', create_category_view, name='create_category'),
    path('create-vegetables/', create_vegetables_view, name='create_vegetable'),

    path('<int:pk>/', include([
        path('vegetables-detail/', vegetables_details_view, name='vegetables-detail'),
        path('vegetables-edit/', edit_vegetables_view, name='vegetables-edit'),
        path('delete-vegetables/', delete_vegetables_view, name='delete-vegetables'),

    ])),

]
