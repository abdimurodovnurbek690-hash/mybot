import os
import telebot
from telebot import types
from openpyxl import Workbook, load_workbook

TOKEN = os.getenv("BOT_TOKEN")

# ⚠️ BU YERGA O'Z TELEGRAM ID INGNI YOZ
ADMIN_ID = 2133751835 

bot = telebot.TeleBot(TOKEN)

# 📦 NARXLAR
prices = {
    "🍎 Olma": 10000,
    "🍌 Banan": 15000
}

user_data = {}

# 📊 EXCEL FUNKSIYA
def save_to_excel(product, price, phone, address):
    file = "orders.xlsx"

    try:
        wb = load_workbook(file)
        ws = wb.active
    except:
        wb = Workbook()
        ws = wb.active
        ws.append(["Mahsulot", "Narx", "Telefon", "Manzil"])

    ws.append([product, price, phone, address])
    wb.save(file)

# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 Buyurtma berish")

    bot.send_message(message.chat.id, "Assalomu alaykum!", reply_markup=markup)

# BUYURTMA
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍎 Olma", "🍌 Banan")

    bot.send_message(message.chat.id, "Mahsulotni tanlang:", reply_markup=markup)

# PRODUCT
@bot.message_handler(func=lambda m: m.text in prices)
def product(message):
    user_data[message.chat.id] = {
        "product": message.text,
        "price": prices.get(message.text, 0)
    }

    btn = types.KeyboardButton("📱 Telefon yuborish", request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon yuboring:", reply_markup=markup)

# PHONE
@bot.message_handler(content_types=['contact'])
def contact(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number

    bot.send_message(message.chat.id, "📍 Manzil yuboring:")

# ADDRESS
@bot.message_handler(func=lambda message: True)
def address(message):
    data = user_data.get(message.chat.id, {})

    product = data.get("product", "Noma'lum")
    price = data.get("price", 0)
    phone = data.get("phone", "Noma'lum")
    address = message.text

    text = (
        f"📥 Yangi buyurtma:\n"
        f"📦 {product}\n"
        f"💰 {price} so'm\n"
        f"📞 {phone}\n"
        f"📍 {address}"
    )

    # 👤 USERGA
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

    # 💳 TO‘LOV TUGMA
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💳 To‘lov qilish", url="https://payme.uz")
    markup.add(btn)

    bot.send_message(message.chat.id, "💰 To‘lovni amalga oshiring:", reply_markup=markup)

    # 👨‍💻 ADMINGA YUBORISH
    bot.send_message(ADMIN_ID, f"🆕 BUYURTMA:\n{text}")

    # 📊 EXCELGA YOZISH
    save_to_excel(product, price, phone, address)

bot.infinity_polling()
