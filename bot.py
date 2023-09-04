import os

import django
import telebot

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avito_notifier.settings")
django.setup()


from bot.models import TelegramUser

bot = telebot.TeleBot("6551507249:AAH5XhUMyWa5e8fDn-Ke6cKq7NrOA44cl-o")


@bot.message_handler(content_types=['text'])
def send_message(message):
    from_user = message.from_user
    chat_id = message.chat.id
    response = "Вы успешно подписались на обновления товаров."
    user = None
    if not TelegramUser.objects.filter(chat_id=chat_id).exists():
        if message.text == '/start':
            user = TelegramUser.objects.create(
                telegram_id=from_user.id,
                first_name=from_user.first_name,
                last_name=from_user.last_name or "",
                username=from_user.username,
                chat_id=chat_id
            )
        else:
            response = "Введите /start чтобы подписаться."
    else:
        user = TelegramUser.objects.get(telegram_id=from_user.id)
        if user.chat_id != chat_id:
            user.chat_id = chat_id
            user.save()
        else:
            response = "Вы уже подписаны на обновления товаров."

    print(user, response)
    bot.send_message(from_user.id, response)


print("Polling messages...")
bot.polling(none_stop=True, interval=1)
