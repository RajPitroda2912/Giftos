from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
@admin.register(user)
class userModelAdmin(UserAdmin):
    model = user
    list_display = ["name", "email", "is_staff", "is_active"]

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone"]

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["name","category","price"]

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

class OrderInline(admin.TabularInline):
    model = OrderDetails

# @admin.register(OrderDetails)
# class OrderDetailsModel(admin.ModelAdmin):
#     list_display = ['product','total','status']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ['user','amount',"payment_id","paid"]