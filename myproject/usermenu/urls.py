from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('content/<int:category>/', views.content, name='content'),
    path('modal_content/<str:product_id>/', views.modal_content, name='modal_content'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
]
