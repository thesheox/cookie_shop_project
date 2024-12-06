from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),  # Signup page
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('orders/', views.order_list, name='order_list'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('products/', views.product_list, name='product_list'),  # Product list
    path('products/add/', views.product_add, name='product_add'),  # Add product
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),  # Edit product
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),  # Delete product
    path('order-groups/', views.order_group_list, name='order_group_list'),  # List order groups
    path('admin-panel/', views.admin_panel, name='admin_panel'),  # Admin panel


]
