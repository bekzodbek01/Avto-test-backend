from django.contrib import admin
from .models import Category, Marathon, Option, OptionAnswer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class MarathonAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    inlines = [OptionInline]

class OptionAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'is_correct', 'answered_at')

admin.site.register(Category)
admin.site.register(Marathon, MarathonAdmin)
admin.site.register(Option)
admin.site.register(OptionAnswer, OptionAnswerAdmin)
