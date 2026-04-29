import telebot
from telebot import types

TOKEN = "8630207711:AAElMiqbNbjeQnN_BTl8lqbzefpS2kO_Vxg"
ADMIN_ID = 2133751835 # o'zingni telegram id

bot = telebot.TeleBot(TOKEN)

orders = []
user_data = {}

# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 Buyurtma berish")

    bot.send_message(message.chat.id, "Assalomu alaykum! Buyurtma berish uchun tugmani bosing 👇", reply_markup=markup)

# BUYURTMA BOSHLASH
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍎 Olma - 10000", "🍌 Banan - 15000")
    markup.add("🔙 Orqaga")

    bot.send_message(message.chat.id, "Mahsulotni tanlang:", reply_markup=markup)

# MAHSULOT TANLASH
@bot.message_handler(func=lambda m: "Olma" in m.text or "Banan" in m.text)
def product(message):
    user_data[message.chat.id] = {}
    user_data[message.chat.id]['product'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📞 Telefon yuborish", request_contact=True)
    markup.add(btn)
    markup.add("🔙 Orqaga")

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)

# TELEFON
@bot.message_handler(content_types=['contact'])
def phone(message):
    user_data[message.chat.id]['phone'] = message.contact.phone_number

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 Orqaga")

    bot.send_message(message.chat.id, "Manzilingizni yozing:", reply_markup=markup)

# MANZIL
@bot.message_handler(func=lambda m: True)
def address(message):

    if message.text == "🔙 Orqaga":
        start(message)
        return

    if message.chat.id not in user_data:
        return

    user_data[message.chat.id]['address'] = message.text

    product = user_data[message.chat.id]['product']
    phone = user_data[message.chat.id]['phone']
    address = user_data[message.chat.id]['address']

    text = f"""
📦 Yangi buyurtma

🛒 {product}
📞 {phone}
📍 {address}
"""

    # ADMIN GA
    bot.send_message(ADMIN_ID, text)

    # SAQLASH
    orders.append(text)

    # USERGA
    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi")

    # TO‘LOV
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💳 To‘lov qilish", url="https://payme.uz/pay")
    markup.add(btn)

    bot.send_message(message.chat.id, "💰 To‘lovni amalga oshiring:", reply_markup=markup)

# 🔙 ORQAGA
@bot.message_handler(func=lambda m: m.text == "🔙 Orqaga")
def back(message):
    start(message)

# ================= ADMIN PANEL =================

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 Buyurtmalar", "🗑 Tozalash")

    bot.send_message(message.chat.id, "⚙️ Admin panel", reply_markup=markup)

# BUYURTMALAR
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtmalar")
def show_orders(message):
    if message.chat.id != ADMIN_ID:
        return

    if not orders:
        bot.send_message(message.chat.id, "❌ Buyurtmalar yo‘q")
        return

    for order in orders:
        bot.send_message(message.chat.id, order)

# TOZALASH
@bot.message_handler(func=lambda m: m.text == "🗑 Tozalash")
def clear_orders(message):
    if message.chat.id != ADMIN_ID:
        return

    orders.clear()
    bot.send_message(message.chat.id, "🧹 Tozalandi")

bot.infinity_polling()
