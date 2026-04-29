import os
import telebot
from telebot import types

# Railway environment variable
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📦 Buyurtma berish")
    markup.add(btn)

    bot.send_message(message.chat.id, "Assalomu alaykum! Buyurtma berish uchun tugmani bosing.", reply_markup=markup)

# BUYURTMA
@bot.message_handler(func=lambda message: message.text == "📦 Buyurtma berish")
def order(message):
    btn = types.KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)

# CONTACT
@bot.message_handler(content_types=['contact'])
def contact(message):
    phone = message.contact.phone_number

    bot.send_message(message.chat.id, "📍 Manzil yuboring yoki yozing (masalan: Chilonzor)")

    bot.register_next_step_handler(message, get_location, phone)

def get_location(message, phone):
    location = message.text

    text = f"""
📦 Yangi buyurtma:
📱 {phone}
📍 {location}
"""

    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

# RUN
print("Bot ishlayapti...")
bot.infinity_polling()
