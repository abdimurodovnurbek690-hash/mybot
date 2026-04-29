import telebot
from telebot import types

TOKEN = "8630207711:AAElMiqbNbjeQnN_BTl8lqbzefpS2kO_Vxg"
ADMIN_ID = 2133751835

bot = telebot.TeleBot(TOKEN)

user_cart = {}
user_step = {}

# START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛍 Katalog", "🛒 Savat")
    bot.send_message(message.chat.id, "Do‘kon botiga xush kelibsiz!", reply_markup=markup)

# KATALOG
@bot.message_handler(func=lambda m: m.text == "🛍 Katalog")
def katalog(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🍎 Olma - 10k", callback_data="olma"))
    markup.add(types.InlineKeyboardButton("🍌 Banan - 15k", callback_data="banan"))
    bot.send_message(message.chat.id, "Mahsulotlar:", reply_markup=markup)

# CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.message.chat.id

    if user_id not in user_cart:
        user_cart[user_id] = []

    if call.data == "olma":
        user_cart[user_id].append("🍎 Olma")
        bot.send_message(user_id, "Olma savatga qo‘shildi")

    elif call.data == "banan":
        user_cart[user_id].append("🍌 Banan")
        bot.send_message(user_id, "Banan savatga qo‘shildi")

# SAVAT
@bot.message_handler(func=lambda m: m.text == "🛒 Savat")
def cart(message):
    user_id = message.chat.id

    if user_id not in user_cart or not user_cart[user_id]:
        bot.send_message(user_id, "🛒 Savat bo‘sh")
        return

    text = "🛒 Savatingiz:\n"
    for item in user_cart[user_id]:
        text += f"- {item}\n"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 Buyurtma berish")

    bot.send_message(user_id, text, reply_markup=markup)

# BUYURTMA
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order(message):
    user_id = message.chat.id

    if user_id not in user_cart or not user_cart[user_id]:
        bot.send_message(user_id, "❗ Savat bo‘sh")
        return

    user_step[user_id] = "phone"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📱 Telefon yuborish", request_contact=True))

    bot.send_message(user_id, "📱 Telefon raqamingizni yuboring:", reply_markup=markup)

# TELEFON
@bot.message_handler(content_types=['contact'])
def get_phone(message):
    user_id = message.chat.id

    if user_step.get(user_id) == "phone":
        user_phone = message.contact.phone_number
        user_step[user_id] = "location"

        user_cart[user_id].append(f"📱 {user_phone}")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("📍 Manzil yuborish", request_location=True))

        bot.send_message(
            user_id,
            "📍 Manzil yuboring yoki yozing (masalan: Chilonzor 5-kvartal)",
            reply_markup=markup
        )

# LOCATION (telefon)
@bot.message_handler(content_types=['location'])
def get_location(message):
    user_id = message.chat.id

    if user_step.get(user_id) == "location":
        lat = message.location.latitude
        lon = message.location.longitude

        order_text = "\n".join(user_cart[user_id])

        bot.send_message(
            ADMIN_ID,
            f"📦 Yangi buyurtma:\n{order_text}\n📍 https://maps.google.com/?q={lat},{lon}"
        )

        send_payment(user_id)

# TEXT LOCATION (desktop)
@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "location" and m.content_type == "text")
def get_text_location(message):
    user_id = message.chat.id

    address = message.text
    order_text = "\n".join(user_cart[user_id])

    bot.send_message(
        ADMIN_ID,
        f"📦 Yangi buyurtma:\n{order_text}\n📍 Manzil: {address}"
    )

    send_payment(user_id)

# TO‘LOV FUNKSIYA
def send_payment(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "💳 To‘lov qilish",
        url="https://payme.uz/home/main"
    ))

    bot.send_message(
        user_id,
        "✅ Buyurtma qabul qilindi!\n💳 To‘lovni amalga oshiring:",
        reply_markup=markup
    )

    user_cart[user_id] = []
    user_step[user_id] = None

# START BOT
bot.infinity_polling()