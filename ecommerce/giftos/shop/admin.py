from django.contrib import admin
from .models import *

class userModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "is_staff", "is_active"]
admin.site.register(user, userModelAdmin)
admin.site.register(Contact)
admin.site.register(Product)


# Register your models here.
