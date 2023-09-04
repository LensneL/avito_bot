import telebot
import requests


TOKEN = "6551507249:AAH5XhUMyWa5e8fDn-Ke6cKq7NrOA44cl-o"

url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

bot = telebot.TeleBot("6551507249:AAH5XhUMyWa5e8fDn-Ke6cKq7NrOA44cl-o")

bot.polling(none_stop=True, interval=0)


@bot.message_handler(content_types=['text'])
def send_message(message, url):
    if message.text == '/start':
        bot.send_message(message.from_user.id, url);
    else:
        bot.send_message(message.from_user.id, 'Напиши /start');
