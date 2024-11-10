# usermenu/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('content/<int:category_id>/', views.content, name='content_with_category'),
    path('modal_content/<str:id_product>/', views.modal_content, name='modal_content'),
    path('search/', views.search, name='search'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('shopping-cart-add/<str:id_product>', views.add_to_cart, name='add_to_cart'),
    path('shopping-cart/remove/<str:id_product>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
