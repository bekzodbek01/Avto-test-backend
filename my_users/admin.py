from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GlobalUserInfo

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('name', 'last_name', 'phone', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('phone', 'name', 'last_name')
    ordering = ('phone',)
    filter_horizontal = ('groups', 'user_permissions')  # Ko'pdan-ko'p munosabatlar uchun qo'shilgan
    fieldsets = (
        (None, {'fields': ('phone',)}),
        ('Personal info', {'fields': ('name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'last_name', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(GlobalUserInfo)
class GlobalUserInfoAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'telegram_username', 'message')
