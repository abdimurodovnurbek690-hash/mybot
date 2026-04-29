import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

user_data = {}

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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🍎 Olma")
    btn2 = types.KeyboardButton("🍌 Banan")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "Mahsulotni tanlang:", reply_markup=markup)

# PRODUCT
@bot.message_handler(func=lambda message: message.text in ["🍎 Olma", "🍌 Banan"])
def product(message):
    user_data[message.chat.id] = {"product": message.text}

    btn = types.KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)

# TELEFON
@bot.message_handler(content_types=['contact'])
def contact(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number

    bot.send_message(message.chat.id, "📍 Manzil yuboring yoki yozing:")

# MANZIL
@bot.message_handler(func=lambda message: True)
def location(message):
    data = user_data.get(message.chat.id, {})

    product = data.get("product", "Noma'lum")
    phone = data.get("phone", "Noma'lum")
    address = message.text

    bot.send_message(message.chat.id,
        f"📦 Yangi buyurtma:\n"
        f"{product}\n"
        f"📞 {phone}\n"
        f"📍 Manzil: {address}"
    )

    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

    # 💳 TO‘LOV TUGMASI (TO‘G‘RI JOYDA)
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💳 To‘lov qilish", url="https://payme.uz")
    markup.add(btn)

    bot.send_message(message.chat.id, "💰 To‘lovni amalga oshiring:", reply_markup=markup)

bot.infinity_polling()
