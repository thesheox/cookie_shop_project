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
    path('logout/', user_logout, name='logout'),
    path('verify/', verify_order, name='verify'),
    path('profile/', profile_page, name='profile'),
    path('profile/edit/<int:pk>/', profile_edit, name='profile_edit'),
    path('cart/delete/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('user/<int:user_id>/addresses/', views.show_addresses, name='show_addresses'),
    path('user/<int:user_id>/add-address/', views.add_address, name='add_address'),
    path('address/<int:address_id>/edit/', views.edit_address, name='edit_address'),
    path('address/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    path('user/<int:user_id>/addresses/set_default/<int:address_id>/', views.set_default_address,
         name='set_default_address'),
    path('20618154.txt', views.zarinpal, name='zarinpal'),
    path('payment/', views.payment, name='payment'),


]



