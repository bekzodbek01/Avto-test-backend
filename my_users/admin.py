
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GlobalUserInfo


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('name', 'last_name', 'phone', 'is_active', 'is_staff')
    list_filter = ('is_active',)
    search_fields = ('phone', 'name', 'last_name')
    ordering = ('phone',)
    fieldsets = (
        (None, {'fields': ('phone',)}),
        ('Shaxsiy ma’lumotlar', {'fields': ('name', 'last_name')}),
        ('Ruxsatlar', {'fields': ('is_staff',  'is_superuser')}),
        ('Muhim sanalar', {'fields': ('last_login',)}),
    )


@admin.register(GlobalUserInfo)
class GlobalUserInfoAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'telegram_username', 'message')
