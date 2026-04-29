import telebot
from telebot import types
import os
from openpyxl import Workbook, load_workbook

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 2133751835 # <-- o'zingni ID qo'y

bot = telebot.TeleBot(TOKEN)

user_data = {}

# 📊 Excel yaratish
file_name = "orders.xlsx"

if not os.path.exists(file_name):
    wb = Workbook()
    ws = wb.active
    ws.append(["Mahsulot", "Narx", "Telefon", "Manzil"])
    wb.save(file_name)

# 🟢 START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📦 Buyurtma berish")
    markup.add(btn)
    bot.send_message(message.chat.id, "Assalomu alaykum! Buyurtma berish uchun tugmani bosing", reply_markup=markup)

# 📦 BUYURTMA
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def buyurtma(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍎 Olma - 10000", "🍌 Banan - 15000")
    bot.send_message(message.chat.id, "Mahsulotni tanlang:", reply_markup=markup)

# 🛒 MAHSULOT
@bot.message_handler(func=lambda m: "Olma" in m.text or "Banan" in m.text)
def product(message):
    if "Olma" in message.text:
        narx = 10000
    else:
        narx = 15000

    user_data[message.chat.id] = {"product": message.text, "price": narx}

    btn = types.KeyboardButton("📞 Telefon yuborish", request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)

# 📞 TELEFON
@bot.message_handler(content_types=['contact'])
def contact(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number
    bot.send_message(message.chat.id, "📍 Manzilni yozing:")

# 📍 MANZIL + YAKUN
@bot.message_handler(func=lambda m: True)
def location(message):
    data = user_data.get(message.chat.id, {})

    if "phone" not in data:
        return

    data["address"] = message.text

    product = data["product"]
    price = data["price"]
    phone = data["phone"]
    address = data["address"]

    # 💳 Payme link
    link = f"https://payme.uz/pay?amount={price*100}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 To‘lov qilish", url=link))

    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!\n💳 To‘lovni amalga oshiring:", reply_markup=markup)

    # 👨‍💻 Adminga yuborish
    bot.send_message(ADMIN_ID,
        f"🆕 Yangi buyurtma:\n\n"
        f"📦 {product}\n"
        f"💰 {price} so'm\n"
        f"📞 {phone}\n"
        f"📍 {address}"
    )

    # 📊 Excelga yozish
    wb = load_workbook(file_name)
    ws = wb.active
    ws.append([product, price, phone, address])
    wb.save(file_name)

    # Excelni adminga yuborish
    bot.send_document(ADMIN_ID, open(file_name, "rb"))

    user_data.pop(message.chat.id)

bot.infinity_polling()
