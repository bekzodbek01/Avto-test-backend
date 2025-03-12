from django.contrib import admin
from .models import Category, Marathon, Option, OptionAnswer
from django.db import models

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

from django.contrib import admin
from django.forms import TextInput, Textarea
from .models import Marathon, Option


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
    }


@admin.register(Marathon)
class MarathonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'category__title')
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_correct', 'marathon')
    list_filter = ('is_correct', 'marathon')


@admin.register(OptionAnswer)
class OptionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'option', 'is_correct')
    list_filter = ('is_correct', 'user')
    search_fields = ('user__username', 'option__text')
