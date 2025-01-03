from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels
from django.utils.functional import cached_property

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images', null=True, blank=True)  # Image field added
    ingredient= models.CharField(max_length=500,null=True, blank=True)
    description=models.CharField(max_length=1000,null=True, blank=True)

    def __str__(self):
        return self.name

class OrderGroup(models.Model):
    DELIVERY_CHOICES = [
        ('تحویل حضوری','تحویل حضوری'),
        ('ارسال با پیک','ارسال با پیک'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = jmodels.jDateTimeField(auto_now_add=True)  # Jalali datetime
    order_number = models.PositiveIntegerField(null=True)
    delivery_method = models.CharField(
        max_length=50,
        choices=DELIVERY_CHOICES,
        default='دریافت حضوری'
    )
    address_line = models.TextField(max_length=255, null=True, blank=True)  # Store the address line directly
    image = models.ImageField(upload_to='order_images/', null=True, blank=True)  # New field for image

    @property
    def date_time(self):
        return str(self.created_at)[:19]

    def __str__(self):
        return f"Order Group {self.id} by {self.user.username}"

    @property
    def total_price(self):
        # Calculate total price by summing the total_price of all related orders
        return sum(order.total_price for order in self.orders.all())  # 'orders' is the related_name of Order model

class Order(models.Model):
    order_group = models.ForeignKey(OrderGroup, related_name='orders', on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} in Order Group {self.order_group.id}"

    @property
    def total(self):
        return self.quantity * self.product.price

from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link Profile to User
#     phone_number = models.CharField(max_length=15, blank=True, null=True)  # Store phone number
#     address = models.TextField(max_length=500, blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user.username}'s profile"


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link Profile to User
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Store phone number
    default_address = models.ForeignKey('Address', null=True, blank=True, on_delete=models.SET_NULL, related_name='default_for')  # Default address link

    def __str__(self):
        return f"{self.user.username}'s profile"

    def set_default_address(self, address):
        """Set the default address for the profile."""
        self.default_address = address
        self.save()

    def clear_default_address(self):
        """Clear the default address for the profile."""
        self.default_address = None
        self.save()



    @cached_property
    def default_address(self):
        # Use the correct related_name to access the addresses
        return self.addresses.filter(is_default=True).first()

class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses')  # Link Address to Profile
    address_line = models.TextField(max_length=255)
    is_default = models.BooleanField(default=False)  # Mark if this is the default address

    def save(self, *args, **kwargs):
        if not hasattr(self, 'profile') or not hasattr(self.profile, 'user'):
            raise ValueError("Address must be linked to a profile with a user.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Address for {self.profile.user.username}: {self.address_line}"
