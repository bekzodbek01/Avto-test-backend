from django.db import models
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Marathon(models.Model):
    category = models.ForeignKey(Category, related_name='marathons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    image = models.ImageField(upload_to='marathons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "No title"


class Option(models.Model):
    marathon = models.ForeignKey(Marathon, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class OptionAnswer(models.Model):
    option = models.ForeignKey(Option, related_name='answers', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    text = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.option:
            self.text = self.option.text
            self.is_correct = self.option.is_correct
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {getattr(self.user, 'username', 'Unknown')} - {self.option.text} - {'Correct' if self.is_correct else 'Incorrect'}"