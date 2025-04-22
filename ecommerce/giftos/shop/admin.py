from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import *


@admin.register(user)
class userModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at", "is_active"]
    list_display_links = ['name','email']

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone"]

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ["name"]

# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ["name","category","price"]

@admin.register(Slider)
class SliderModelAdmin(admin.ModelAdmin):
    list_display = ["id","name"]

class CartInline(admin.TabularInline):
    model = CartItem
    extra = 1

# @admin.register(CartItem)
# class CartItemModelAdmin(admin.ModelAdmin):
#     list_display = ["product", "quantity"]

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    inlines = [CartInline]
    list_display = ["user"]

class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 1

# @admin.register(OrderDetails)
# class OrderDetailsModelAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'total', 'status']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    inlines = [OrderDetailsInline]
    list_display = ['user', 'amount', 'payment_id', 'paid', 'created_at', 'updated_at']
  

class AdminNotificationForm(forms.ModelForm):
    class Meta:
        model = AdminNotification
        fields = ['message', 'notification_type']

@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    form = AdminNotificationForm
    list_display = ['message', 'notification_type', 'created_at']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Send notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'user_notifications',  # Ensure this matches the group name in your consumer
            {
                'type': 'send_notification',  # Ensure this matches the method name in your consumer
                'message': obj.message,  # Send the actual message from the AdminNotification object
            }
    )
        
        # Optionally associate with all users
        obj.users.set(user.objects.all())