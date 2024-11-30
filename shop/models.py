from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # Import settings to use the custom user model

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name="full_name")
    phone_number = models.CharField(max_length=15, verbose_name="phone_number")
    email = models.EmailField(unique=True, verbose_name="email")

    # Add related_name to avoid clashes with the default User model's groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related_name
        blank=True,
        verbose_name='گروه‌ها'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Custom related_name
        blank=True,
        verbose_name='دسترسی‌ها'
    )

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images', null=True, blank=True)  # Image field added

    def __str__(self):
        return self.name

class OrderGroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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
