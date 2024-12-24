import random

from django.core.files.storage import default_storage
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

@login_required
def admin_panel(request):

    return render(request, 'shop/admin_panel.html')
from datetime import date
def order_group_list(request):
    # Filter objects created today and order them by created_at in descending order
    order_groups = OrderGroup.objects.filter(created_at__date=date.today()).order_by('-created_at')

    return render(request, 'shop/order_group_list.html', {'order_groups': order_groups})



@login_required
def profile_page(request):
    return render(request, 'shop/profile_page.html')

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
        product.name = request.POST.get('product_name')
        product.price = request.POST.get('product_price')
        product.quantity = request.POST.get('product_quantity')
        product.ingredient = request.POST.get('product_materials')
        product.description = request.POST.get('product_description')

        # Handle file upload if applicable
        if 'product_image' in request.FILES:
            # Delete old image if it exists
            if product.image:
                if default_storage.exists(product.image.path):
                    default_storage.delete(product.image.path)
            product.image = request.FILES['product_image']

        # Save the updated product
        product.save()

        # Redirect to product list page
        return redirect('product_list')

    return render(request, 'shop/product_edit.html', {'product': product, 'title': 'ویرایش محصول'})



def profile_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        # Get the updated values from the POST data
        full_name = request.POST.get('user_name').split(' ')
        print(full_name)
        user.first_name = full_name[0]
        user.last_name = full_name[1]

        user.email= request.POST.get('user_email')
        # User = request.POST.get('product_materials')
        # product.description = request.POST.get('product_description')

        profile.phone_number=request.POST.get('user_phone_number')



        # Save the updated product
        user.save()
        profile.save()

        # Redirect to product list page
        return redirect('profile')

    return render(request, 'shop/profile_edit.html', {'user': user, 'profile':profile , 'title': 'ویرایش محصول'})

def product_delete(request, pk):
    if request.method == 'POST':  # Confirm deletion
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, f'Product "{product.name}" has been deleted.')
        return redirect('product_list')


@login_required
def checkout(request):
    # Get the cart stored in session
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')  # Redirect to cart if no items


    import random

    # Set to keep track of already generated numbers
    generated_numbers = set()

    def generate_one_unique_random(start, end):
        if len(generated_numbers) >= (end - start + 1):
            raise ValueError("All possible unique numbers have been generated.")

        while True:
            number = random.randint(start, end)
            if number not in generated_numbers:
                generated_numbers.add(number)
                return number

    # Example usage

    # Create a new OrderGroup
    order_group = OrderGroup.objects.create(user=request.user,order_number=generate_one_unique_random(1000000, 9999999))

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
            total_price=product.price * quantity,
        )

    # After creating orders, clear the cart
    request.session['cart'] = {}

    # Redirect to order list after checkout
    return redirect('verify')

@login_required
def verify_order(request):
    order_groups = OrderGroup.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'shop/verify_page.html',{'order_groups': order_groups[0]})
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
            return redirect('home')
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است", extra_tags="login")

    return render(request, 'shop/login.html')

import re
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
            messages.error(request, 'تمامی فیلدها اجباری هستند.', extra_tags="signup")
            return render(request, 'shop/signup.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'رمزهای عبور مطابقت ندارند.', extra_tags="signup")
            return render(request, 'shop/signup.html')

            # Password strength check
        if len(password) < 8:
            messages.error(request, 'رمز عبور باید حداقل ۸ کاراکتر باشد.', extra_tags="signup")
            return render(request, 'shop/signup.html')

        if not re.search(r'[A-Za-z]', password):
            messages.error(request, 'رمز عبور باید شامل حداقل یک حرف باشد.', extra_tags="signup")
            return render(request, 'shop/signup.html')

        if not re.search(r'[0-9]', password):
            messages.error(request, 'رمز عبور باید شامل حداقل یک عدد باشد.', extra_tags="signup")
            return render(request, 'shop/signup.html')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'رمز عبور باید شامل حداقل یک کاراکتر خاص باشد.', extra_tags="signup")
            return render(request, 'shop/signup.html')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'نام کاربری قبلا ثبت شده است.', extra_tags="signup")
            return render(request, 'shop/signup.html')


        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'ایمیل قبلا ثبت شده است.', extra_tags="signup")
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
                'total_price_sale': product.price*quantity,
            }

        request.session['cart'] = cart  # Save cart to session
        return redirect('cart')  # Redirect to the cart page after adding

    return render(request, 'shop/buy_product.html', {'product': product})

@login_required
def cart(request):
    user = request.user

    # Get the default address for the user, if it exists
    try:
        default_address = user.profile.default_address
    except AttributeError:
        default_address = None

    cart = request.session.get('cart', {})  # Retrieve cart from session
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())  # Calculate total price
    return render(request, 'shop/cart.html', {'cart': cart, 'total_price': total_price,'default_address': default_address})

@login_required
def delete_cart_item(request, product_id):
    # Retrieve the cart from the session
    cart = request.session.get('cart', {})

    # Check if the product is in the cart
    if str(product_id) in cart:
        del cart[str(product_id)]  # Remove the item from the cart

        # Update the session
        request.session['cart'] = cart
        messages.success(request, 'Item removed from the cart.')

    return redirect('cart')  # Redirect back to the cart page


from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Address
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Address
from django.contrib.auth.models import User

def show_addresses(request, user_id):
    user = get_object_or_404(User, id=user_id)
    addresses = Address.objects.filter(profile=user.profile)
    return render(request, 'shop/show_addresses.html', {'user': user, 'addresses': addresses})

def add_address(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    if request.method == "POST":
        address_line = request.POST.get('address_line', '').strip()
        if address_line:
            Address.objects.create(profile=profile, address_line=address_line)
            return redirect('show_addresses', user_id=user_id)
    return render(request, 'shop/add_address.html', {'user': profile.user})

def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == "POST":
        new_address_line = request.POST.get('address_line', '').strip()
        if new_address_line:
            address.address_line = new_address_line
            address.save()
            return redirect('show_addresses', user_id=address.profile.user.id)
    return render(request, 'shop/edit_address.html', {'address': address})

def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    user_id = address.profile.user.id
    if request.method == "POST":
        address.delete()
    return redirect('show_addresses', user_id=user_id)


from django.shortcuts import get_object_or_404, redirect
from .models import Profile, Address

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Profile, Address


# def set_default_address(request, user_id):
#     if request.method == "POST":
#         user = get_object_or_404(User, id=user_id)
#         address_id = request.POST.get('default_address')
#
#         # Debugging: Check if address_id is received properly
#         print(f"Received address_id: {address_id}")
#
#         if address_id:
#             address = get_object_or_404(Address, id=address_id)
#             profile = user.profile
#             profile.default_address = address
#             profile.save()
#
#             print("Default address updated.")  # Debugging message
#         else:
#             print("No address selected.")  # Debugging message
#
#     return redirect('show_addresses', user_id=user_id)


from django.shortcuts import get_object_or_404, redirect
from .models import Profile, Address
from django.contrib import messages


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User, Address

def set_default_address(request, user_id, address_id):
    user = get_object_or_404(User, id=user_id)
    address = get_object_or_404(Address, id=address_id)

    # Get the profile associated with the user
    profile = user.profile

    # Set the selected address as the default
    profile.default_address = address

    # Unmark other addresses as default
    Address.objects.filter(profile=profile).exclude(id=address.id).update(is_default=False)

    # Mark the selected address as default
    address.is_default = True

    # Save the changes to both the address and profile
    address.save()
    profile.save()

    # Show a success message
    messages.success(request, f'Address "{address.address_line}" set as default.')

    # Redirect to the page showing the list of addresses
    return redirect('show_addresses', user_id=user_id)


def zarinpal(request):
    return render(request, 'shop/zarinpal.txt')