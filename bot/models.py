from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True)
    chat_id = models.PositiveIntegerField(unique=True, db_index=True )
    subscribed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.telegram_id}) - {self.chat_id}"
