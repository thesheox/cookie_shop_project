from django.db import models
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link Profile to User
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Store phone number

    def __str__(self):
        return f"{self.user.username}'s profile"
