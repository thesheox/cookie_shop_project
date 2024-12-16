from django.contrib import admin
from .models import Product, Order, OrderGroup

# Inline for Order
class OrderInline(admin.TabularInline):
    model = Order
    extra = 0  # No extra empty forms by default
    readonly_fields = ('product', 'quantity', 'total_price')  # Make these fields read-only
    can_delete = False  # Disable deletion of orders from here

    # Override to calculate the total price of an order
    def total_price(self, obj):
        return obj.product.price * obj.quantity
    total_price.short_description = 'Total Price'

# Admin for OrderGroup
@admin.register(OrderGroup)
class OrderGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price','order_number')  # Fields to display in the list view
    inlines = [OrderInline]  # Add Order inline to OrderGroup
    readonly_fields = ('user', 'created_at')  # Make these fields read-only
    ordering = ('-created_at',)  # Order by the newest checkout first

    # Calculate the total price of the order group
    def total_price(self, obj):
        # Sum the total prices of all orders in this OrderGroup
        total = sum(order.product.price * order.quantity for order in obj.orders.all())
        return total
    total_price.short_description = 'Total Price'

# Admin for Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity')  # Display these fields
    search_fields = ('name',)  # Add search by product name

# Admin for Order (Optional)
from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  # Show user and phone_number in the list view
    search_fields = ('user__username', 'phone_number')  # Allow searching by username and phone number
    list_filter = ('user',)  # Filter by user


admin.site.register(Profile, ProfileAdmin)  # Register the Profile model with custom admin options
