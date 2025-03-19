from django.db import models
from django.contrib.auth.models import User


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
