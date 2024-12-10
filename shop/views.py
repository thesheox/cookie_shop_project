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
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('home')  # پس از خروج، کاربر به صفحه اصلی هدایت می‌شود

def admin_panel(request):
    return render(request, 'shop/admin_panel.html')

def order_group_list(request):
    order_groups = OrderGroup.objects.all().order_by('-created_at')  # Order by newest first
    return render(request, 'shop/order_group_list.html', {'order_groups': order_groups})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# View for adding a new product
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ProductForm

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Product  # Import your Product model

def product_add(request):
    if request.method == 'POST':
        # Extract data from the POST request
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_quantity = request.POST.get('product_quantity')
        product_materials = request.POST.get('product_materials')
        product_description = request.POST.get('product_description')
        product_image = request.FILES.get('product_image')

        # Validation checks (optional)
        if not product_name or not product_price or not product_quantity:
            messages.error(request, 'لطفاً تمام فیلدهای ضروری را پر کنید.')
        else:
            try:
                # Create and save a new product instance
                Product.objects.create(
                    name=product_name,
                    price=product_price,
                    quantity=product_quantity,
                    ingredient=product_materials,
                    description=product_description,
                    image=product_image,
                )
                messages.success(request, 'محصول با موفقیت اضافه شد.')
                return redirect('product_list')
            except Exception as e:
                messages.error(request, f'خطایی رخ داد: {e}')

    return render(request, 'shop/product_form.html', {'title': 'اضافه کردن محصولات'})

# View for editing an existing product
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # Get the updated values from the POST data
        product.product_name = request.POST.get('product_name')
        product.product_price = request.POST.get('product_price')
        product.product_quantity = request.POST.get('product_quantity')
        product.product_materials = request.POST.get('product_materials')
        product.product_description = request.POST.get('product_description')

        # Handle file upload if applicable
        if 'product_image' in request.FILES:
            product.product_image = request.FILES['product_image']

        # Save the updated product
        product.save()

        # Redirect to product list page
        return redirect('product_list')

    return render(request, 'shop/product_edit.html', {'product': product, 'title': 'ویرایش محصول'})

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
    return redirect('verify')

@login_required
def verify_order(request):
    return render(request,'shop/verify_page.html')
@login_required
def order_list(request):
    # Get the orders grouped by OrderGroup
    order_groups = OrderGroup.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_list.html', {'order_groups': order_groups})


def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return render(request, 'shop/login.html')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'shop/login.html')


def user_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()

        # Check for empty fields
        if not full_name or not username or not password or not confirm_password or not email:
            messages.error(request, 'All fields are required.')
            return render(request, 'shop/signup.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'shop/signup.html')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'shop/signup.html')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return render(request, 'shop/signup.html')

        # Split full name into first and last names
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.save()

        # Create the profile
        Profile.objects.create(user=user, phone_number=phone_number)

        messages.success(request, 'Account created successfully. You are now logged in.')
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



