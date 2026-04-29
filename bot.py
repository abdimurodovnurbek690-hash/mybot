import telebot
from telebot import types

TOKEN = "8630207711:AAElMiqbNbjeQnN_BTl8lqbzefpS2kO_Vxg"
ADMIN_ID = 2133751835  # o'zingni telegram ID

bot = telebot.TeleBot(TOKEN)

user_data = {}

# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📦 Buyurtma berish")
    markup.add(btn)

    bot.send_message(message.chat.id, "Assalomu alaykum!\nBuyurtma berish uchun tugmani bosing.", reply_markup=markup)


# BUYURTMA BOSHLASH
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍎 Olma - 10000", "🍌 Banan - 15000")

    bot.send_message(message.chat.id, "Mahsulotni tanlang:", reply_markup=markup)


# MAHSULOT TANLASH
@bot.message_handler(func=lambda m: "Olma" in m.text or "Banan" in m.text)
def product(message):
    user_data[message.chat.id] = {"product": message.text}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📱 Telefon yuborish", request_contact=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)


# TELEFON
@bot.message_handler(content_types=['contact'])
def contact(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number

    bot.send_message(message.chat.id, "📍 Manzilingizni yozing:")


# MANZIL
@bot.message_handler(func=lambda m: m.chat.id in user_data and "phone" in user_data[m.chat.id])
def address(message):
    user_data[message.chat.id]["address"] = message.text

    data = user_data[message.chat.id]

    text = f"""
🆕 YANGI BUYURTMA

📦 Mahsulot: {data['product']}
📱 Telefon: {data['phone']}
📍 Manzil: {data['address']}
"""

    # Adminga yuborish
    bot.send_message(ADMIN_ID, text)

    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

    user_data.pop(message.chat.id)


bot.infinity_polling()
