from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderGroup
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

# View for listing all products
from .models import OrderGroup, Order
from django.shortcuts import render

def admin_panel(request):
    return render(request, 'shop/admin_panel.html')

def order_group_list(request):
    order_groups = OrderGroup.objects.all().order_by('-created_at')  # Order by newest first
    return render(request, 'shop/order_group_list.html', {'order_groups': order_groups})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# View for adding a new product
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Add Product'})

# View for editing an existing product
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Edit Product'})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':  # Confirm deletion
        product.delete()
        messages.success(request, f'Product "{product.name}" has been deleted.')
        return redirect('product_list')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})
@login_required
def checkout(request):
    # Get the cart stored in session
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')  # Redirect to cart if no items

    # Create a new OrderGroup
    order_group = OrderGroup.objects.create(user=request.user)

    # Initialize total price
    total_price = 0

    # Loop through cart and create an order for each product
    for product_id, item in cart.items():
        # Retrieve the product
        product = get_object_or_404(Product, id=product_id)

        # Get quantity from the cart item (assuming it's stored as a dictionary)
        quantity = item.get('quantity', 1)  # Default to 1 if quantity is not found

        # Calculate the total price for the product
        total_price += product.price * quantity

        # Create an order item in the Order model
        Order.objects.create(
            order_group=order_group,
            product=product,
            quantity=quantity,
            total_price=product.price * quantity
        )

    # After creating orders, clear the cart
    request.session['cart'] = {}

    # Redirect to order list after checkout
    return redirect('order_list')


@login_required
def order_list(request):
    # Get the orders grouped by OrderGroup
    order_groups = OrderGroup.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_list.html', {'order_groups': order_groups})


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
        # Get data from form
        full_name = request.POST['full_name']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        email = request.POST['email']

        # Check if password and confirm_password match
        if password != confirm_password:
            return render(request, 'shop/signup.html', {'error': 'Passwords do not match'})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'shop/signup.html', {'error': 'Username already exists'})

        # Split full name into first name and last name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Create user
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                        last_name=last_name, email=email)

        user.save()
        Profile.objects.create(user=user,phone_number = phone_number )

        # Log the user in
        login(request, user)
        return redirect('home')

    return render(request, 'shop/signup.html')


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})  # Use session to store cart data

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not specified
        if quantity > product.quantity:
            # If quantity exceeds stock, show an error
            return render(request, 'shop/buy_product.html', {
                'product': product,
                'error': f'Not enough stock available. Current stock: {product.quantity}',
            })

        # Decrease the quantity of the product in the database
        product.quantity -= quantity
        product.save()  # Save the updated quantity to the database

        # Add or update product in the cart
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity  # Update quantity
        else:
            cart[str(product_id)] = {
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'image': product.image.url if product.image else '',  # Handle image if available
            }

        request.session['cart'] = cart  # Save cart to session
        return redirect('cart')  # Redirect to the cart page after adding

    return render(request, 'shop/buy_product.html', {'product': product})

@login_required
def cart(request):
    cart = request.session.get('cart', {})  # Retrieve cart from session
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())  # Calculate total price
    return render(request, 'shop/cart.html', {'cart': cart, 'total_price': total_price})



