from django.db import models
from django.contrib.auth.models import User
import random


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title or 'No title'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'


class Marathon(models.Model):
    category = models.ForeignKey(Category, related_name="marathons", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="marathons/", blank=True, null=True)

    def __str__(self):
        return self.title or 'No title'

    class Meta:
        verbose_name = 'Marathon'
        verbose_name_plural = 'Marathon'


class Option(models.Model):
    marathon = models.ForeignKey(Marathon, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    extra_info = models.TextField(blank=True, null=True)  # Qo‘shimcha maydon
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text or 'No title'

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Option'


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(Option)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} - Correct: {self.is_correct}"


# class Ticket(models.Model):
#     """Biletlar modeli, marafonga bog‘langan"""
#     marathon = models.ForeignKey(Marathon, related_name="tickets", on_delete=models.CASCADE)
#     questions = models.ManyToManyField(Option)
#
#     @classmethod
#     def generate_tickets(cls, marathon, user):
#         """Marafondagi savollarni 20 tadan bo‘lib bilet yaratish va foydalanuvchiga bog‘lash"""
#         options = marathon.options.order_by("id")  # ID bo‘yicha tartiblash
#         ticket_questions = []
#         tickets = []
#
#         for option in options:
#             ticket_questions.append(option)  # Savolni biletga qo‘shish
#
#             # 20 taga yetganda bilet yaratamiz
#             if len(ticket_questions) == 20:
#                 ticket = cls.objects.create(marathon=marathon)
#                 ticket.questions.set(ticket_questions)  # Savollarni bog‘lash
#                 UserTicket.objects.create(user=user, ticket=ticket)  # Foydalanuvchiga biriktirish
#                 tickets.append(ticket)
#                 ticket_questions = []  # Yangi bilet uchun tozalash
#
#         # Oxirgi bilet 20 tadan kam bo‘lsa, lekin savollar qolgan bo‘lsa
#         if ticket_questions:
#             ticket = cls.objects.create(marathon=marathon)
#             ticket.questions.set(ticket_questions)
#             UserTicket.objects.create(user=user, ticket=ticket)  # Foydalanuvchiga bog‘lash
#             tickets.append(ticket)
#
#         return tickets  # Yaratilgan barcha biletlarni qaytaramiz
#
#
# class UserTicket(models.Model):
#     """Foydalanuvchiga ajratilgan biletlar"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} uchun {self.ticket.id}-bilet"
