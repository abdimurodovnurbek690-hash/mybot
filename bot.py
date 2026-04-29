import telebot
from telebot import types
from openpyxl import Workbook, load_workbook
import os

TOKEN = "8630207711:AAElMiqbNbjeQnN_BTl8lqbzefpS2kO_Vxg"
ADMIN_ID = 2133751835  # o'zingni telegram ID yoz

bot = telebot.TeleBot(TOKEN)

user_data = {}

# Excel fayl yaratish
if not os.path.exists("orders.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.append(["Mahsulot", "Narx", "Telefon", "Manzil"])
    wb.save("orders.xlsx")


# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📦 Buyurtma berish")
    markup.add(btn)

    bot.send_message(message.chat.id, "Assalomu alaykum! Buyurtma berish uchun tugmani bosing.", reply_markup=markup)


# BUYURTMA BOSHLASH
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍎 Olma - 10000", "🍌 Banan - 15000")

    bot.send_message(message.chat.id, "Mahsulotni tanlang:", reply_markup=markup)


# MAHSULOT TANLASH
@bot.message_handler(func=lambda m: "Olma" in m.text or "Banan" in m.text)
def product(message):
    if "Olma" in message.text:
        narx = 10000
    else:
        narx = 15000

    user_data[message.chat.id] = {
        "product": message.text,
        "price": narx
    }

    btn = types.KeyboardButton("📱 Telefon yuborish", request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)


# TELEFON
@bot.message_handler(content_types=['contact'])
def contact(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number

    bot.send_message(message.chat.id, "📍 Manzilni yozing:")


# MANZIL + YAKUNIY
@bot.message_handler(func=lambda m: True)
def location(message):
    data = user_data.get(message.chat.id)

    if not data:
        return

    data["address"] = message.text

    text = f"""
🆕 Yangi buyurtma:

📦 {data['product']}
💰 {data['price']} so'm
📱 {data['phone']}
📍 {data['address']}
"""

    # USERGA
    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

    # TO‘LOV TUGMA
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        "💳 To‘lov qilish",
        url="https://payme.uz/pay"
    )
    markup.add(btn)

    bot.send_message(message.chat.id, "💰 To‘lovni amalga oshiring:", reply_markup=markup)

    # ADMINGA YUBORISH
    bot.send_message(ADMIN_ID, text)

    # EXCELGA YOZISH
    wb = load_workbook("orders.xlsx")
    ws = wb.active
    ws.append([
        data['product'],
        data['price'],
        data['phone'],
        data['address']
    ])
    wb.save("orders.xlsx")

    # TOZALASH
    user_data.pop(message.chat.id)


bot.infinity_polling()
