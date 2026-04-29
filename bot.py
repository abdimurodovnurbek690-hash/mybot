import telebot
from telebot import types
from openpyxl import Workbook, load_workbook
import os

TOKEN = 8630207711:AAElMiqbNbjeQnN_BTl8lqbzefpS2kO_Vxg   # <-- bu yerga token
ADMIN_ID = 2133751835        # <-- bu yerga o'zingni ID

bot = telebot.TeleBot(TOKEN)

user_data = {}

# Excel fayl yaratish
if not os.path.exists("orders.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.append(["Ism", "Telefon", "Mahsulot", "Narx", "Manzil"])
    wb.save("orders.xlsx")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📦 Buyurtma berish")
    markup.add(btn)

    bot.send_message(message.chat.id, "Assalomu alaykum! Buyurtma berish uchun tugmani bosing 👇", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🍎 Olma - 10000", "🍌 Banan - 15000")

    bot.send_message(message.chat.id, "Mahsulotni tanlang:", reply_markup=markup)


@bot.message_handler(func=lambda m: "Olma" in m.text or "Banan" in m.text)
def product(message):
    user_data[message.chat.id] = {}

    if "Olma" in message.text:
        user_data[message.chat.id]["product"] = "Olma"
        user_data[message.chat.id]["price"] = 10000
    else:
        user_data[message.chat.id]["product"] = "Banan"
        user_data[message.chat.id]["price"] = 15000

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📱 Telefon yuborish", request_contact=True)
    markup.add(btn)

    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def contact(message):
    user_data[message.chat.id]["phone"] = message.contact.phone_number

    bot.send_message(message.chat.id, "📍 Manzilingizni yozing:")
    bot.register_next_step_handler(message, address)


def address(message):
    user_data[message.chat.id]["address"] = message.text

    data = user_data[message.chat.id]

    # Excelga yozish
    wb = load_workbook("orders.xlsx")
    ws = wb.active
    ws.append([
        message.from_user.first_name,
        data["phone"],
        data["product"],
        data["price"],
        data["address"]
    ])
    wb.save("orders.xlsx")

    # Adminga yuborish
    text = f"""
🆕 Yangi buyurtma:

👤 {message.from_user.first_name}
📦 {data['product']}
💰 {data['price']} so'm
📱 {data['phone']}
📍 {data['address']}
"""
    bot.send_message(ADMIN_ID, text)

    # To‘lov link (PAYME)
    amount = data["price"] * 100  # tiyin
    link = f"https://payme.uz/pay?amount={amount}"

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💳 To‘lov qilish", url=link)
    markup.add(btn)

    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!\nTo‘lovni amalga oshiring:", reply_markup=markup)


bot.polling()
