from django.contrib import admin
from .models import Category, Marathon, Option, UserAnswer


class OptionInline(admin.TabularInline):
    model = Option
    extra = 2  # Har bir marafon uchun 2 variant oldindan chiqadi


@admin.register(Marathon)
class MarathonAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    fields = ('category', 'title', 'text', 'image')
    list_filter = ['category']
    inlines = [OptionInline]  # Option inlines


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


admin.site.register(UserAnswer)
admin.site.register(Category)
