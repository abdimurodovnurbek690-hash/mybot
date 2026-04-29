import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# 📦 NARXLAR
prices = {
    "🍎 Olma": 10000,
    "🍌 Banan": 15000
}

user_data = {}

# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 Buyurtma berish")

    bot.send_message(message.chat.id, "Assalomu alaykum! Tugmani bosing:", reply_markup=markup)

# BUYURTMA
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍎 Olma", "🍌 Banan")

    bot.send_message(message.chat.id, "Mahsulotni tanlang:", reply_markup=markup)

# PRODUCT
@bot.message_handler(func=lambda m: m.text in ["🍎 Olma", "🍌 Banan"])
def product(message):
    user_data[message.chat.id] = {
        "product": message.text,
        "price": prices.get(message.text, 0)
    }

    btn = types.KeyboardButton("📱 Telefon yuborish", request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)

# PHONE
@bot.message_handler(content_types=['contact'])
def contact(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number

    bot.send_message(message.chat.id, "📍 Manzil yuboring yoki yozing:")

# ADDRESS (YAKUNIY)
@bot.message_handler(func=lambda message: True)
def address(message):
    data = user_data.get(message.chat.id, {})

    product = data.get("product", "Noma'lum")
    phone = data.get("phone", "Noma'lum")
    price = data.get("price", 0)
    address = message.text

    bot.send_message(
        message.chat.id,
        f"📥 Yangi buyurtma:\n"
        f"📦 Mahsulot: {product}\n"
        f"💰 Narx: {price} so'm\n"
        f"📞 Telefon: {phone}\n"
        f"📍 Manzil: {address}"
    )

    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

bot.infinity_polling()
