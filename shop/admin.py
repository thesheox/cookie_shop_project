from django.contrib import admin
from .models import Product, Order, OrderGroup
from django.utils.functional import cached_property

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


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone_number')  # Show user and phone_number in the list view
#     search_fields = ('user__username', 'phone_number')  # Allow searching by username and phone number
#     list_filter = ('user',)  # Filter by user
#
#
# admin.site.register(Profile, ProfileAdmin)  # Register the Profile model with custom admin options

from django.contrib import admin
from .models import Profile, Address
from django import forms

from django.contrib import admin
from .models import Profile, Address
from django import forms

# Inline form for managing addresses in Profile admin
class AddressInline(admin.TabularInline):
    model = Address
    extra = 1  # Add one blank form for new address
    fields = ['address_line', 'is_default']  # Show address line and default checkbox
    max_num = None  # Allow unlimited addresses

    # Ensure only one default address per profile
    def save_model(self, request, obj, form, change):
        if obj.is_default:
            # Update all other addresses to be non-default for this profile
            Address.objects.filter(profile=obj.profile).exclude(id=obj.id).update(is_default=False)
        super().save_model(request, obj, form, change)

# Custom form to edit the default address field in the Profile admin
class ProfileForm(forms.ModelForm):
    default_address = forms.ModelChoiceField(queryset=Address.objects.all(), required=False, label='Default Address')

    class Meta:
        model = Profile
        fields = ['user', 'phone_number', 'default_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preselect the current default address for the Profile
        if self.instance and self.instance.default_address:
            self.fields['default_address'].initial = self.instance.default_address

# Profile admin with inline Address management
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'default_address_display']  # Show user, phone, and default address
    search_fields = ['user__username', 'phone_number']  # Search by username or phone
    inlines = [AddressInline]  # Add AddressInline for managing addresses
    form = ProfileForm  # Use the custom form

    # Display default address in the profile list
    def default_address_display(self, obj):
        return obj.default_address.address_line if obj.default_address else 'No default address'
    default_address_display.short_description = 'Default Address'

    # Allow editing the default address in the form
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        # You can add additional logic here to filter the available addresses if needed
        return form

# Address admin to manage individual addresses
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['profile', 'address_line', 'is_default']  # Show profile, address line, and default status
    search_fields = ['address_line', 'profile__user__username']  # Search by address or user
