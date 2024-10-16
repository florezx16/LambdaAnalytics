from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ['username','first_name','last_name','is_staff','is_active']

admin.site.register(CustomUser, CustomUserAdmin)