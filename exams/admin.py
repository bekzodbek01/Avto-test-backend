from django.contrib import admin
from .models import Category, Marathon, Option


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


admin.site.register(Category)

#
#
# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ('marathon',)
#     search_fields = ('marathon__title',)
#     filter_horizontal = ('questions',)
#
#
# @admin.register(UserTicket)
# class UserTicketAdmin(admin.ModelAdmin):
#     list_display = ('user', 'ticket', 'created_at')
#     search_fields = ('user__username', 'ticket__marathon__title')
#
#
# @admin.register(UserTicketResult)
# class UserTicketResultAdmin(admin.ModelAdmin):
#     list_display = ('user_ticket', 'total_correct_answers', 'total_incorrect_answers', 'correct_percentage')
#     search_fields = ('user_ticket__user__username', 'user_ticket__ticket__marathon__title')
#     list_filter = ('correct_percentage',)