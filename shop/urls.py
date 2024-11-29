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

]
