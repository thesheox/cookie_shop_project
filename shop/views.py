from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'shop/login.html', {'error': 'Invalid credentials'})
    return render(request, 'shop/login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'shop/signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'shop/signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)
        return redirect('home')

    return render(request, 'shop/signup.html')

@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        if quantity > product.quantity:
            return render(request, 'shop/buy_product.html', {'product': product, 'error': 'Not enough stock'})
        total_price = quantity * product.price
        product.quantity -= quantity
        product.save()
        Order.objects.create(user=request.user, product=product, quantity=quantity, total_price=total_price)
        return redirect('order_list')
    return render(request, 'shop/buy_product.html', {'product': product})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_list.html', {'orders': orders})

def cart(request):
    return render(request, 'shop/cart.html')





