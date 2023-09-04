from django.db import models


class Offer(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    link = models.URLField(max_length=256)
    added_at = models.DateTimeField(auto_now_add=True)
    keep = models.BooleanField(default=False)
    photo = models.ImageField()


class TelegramUser(models.Model):
    username = models.CharField(max_length=32)
    chat_id = models.CharField(max_length=128)
