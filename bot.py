import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8180676876:AAFYW474VRX9auFWIhAjANahGuBvCSoUNQY"
ADMIN_ID = "1369109422"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Foydalanuvchilarning hisobini saqlash
user_balances = {}

async def get_bot_username():
    global BOT_USERNAME
    BOT_USERNAME = (await bot.get_me()).username

# **Bosh menyu tugmalari**
main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="📦 Ovoz berish"), KeyboardButton(text="💰 Hisobim")],
        [KeyboardButton(text="🏦 Pul yechib olish")],
        [KeyboardButton(text="🎉 Konkurs"), KeyboardButton(text="👥 Referal")],
        [KeyboardButton(text="ℹ️ Qo‘llanma")]
    ]
)

# **/start komandasi - Kontakt so‘rash**
@dp.message(Command("start"))
async def start_command(message: types.Message):
    contact_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text="📞 Kontaktni ulashish", request_contact=True)]]
    )
    await message.answer("👋 Assalomu alaykum! Botdan foydalanish uchun kontaktni ulashing.", reply_markup=contact_keyboard)

# **Kontakt qabul qilish**
@dp.message(F.contact)
async def get_contact(message: types.Message):
    user_id = message.from_user.id
    user_balances[user_id] = {"balance": 0}  # Foydalanuvchi uchun hisob yaratish
    await message.answer("✅ Kontakt qabul qilindi! Endi bosh menyudan foydalanishingiz mumkin.", reply_markup=main_keyboard)

# **📦 Ovoz berish**
@dp.message(F.text == "📦 Ovoz berish")
async def vote_command(message: types.Message):
    vote_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="✅ Ovoz berdim")],
            [KeyboardButton(text="🔙 Orqaga")]
        ]
    )
    vote_link = "https://openbudget.uz/boards/initiatives/initiative/50/28d38d89-9ab1-4dc7-a538-b3e06e76a6c0"
    await message.answer(
        f"Ovoz berish uchun quyidagi havolani bosing:\n\n"
        f"🔗 {vote_link}\n\n"
        f"So‘ng 'Ovoz berdim' tugmasini bosing!",
        reply_markup=vote_keyboard
    )

# **✅ Ovoz berdim - Skrinshot so‘rash**
@dp.message(F.text == "✅ Ovoz berdim")
async def confirm_vote(message: types.Message):
    await message.answer("📸 Iltimos, ovoz berganingizni tasdiqlash uchun skrinshot yuboring!")

# **📸 Skrinshot yuborish**
@dp.message(F.photo)
async def handle_screenshot(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Ismi yo‘q"

    # Foydalanuvchiga 20 000 so‘m qo‘shish
    if user_id not in user_balances:
        user_balances[user_id] = {"balance": 0}
    user_balances[user_id]["balance"] += 20000  

    # Skrinshotni adminga yuborish
    photo = message.photo[-1].file_id  
    caption = f"📥 **Yangi skrinshot!**\n👤 @{username}\n🆔 ID: {user_id}"
    await bot.send_photo(ADMIN_ID, photo=photo, caption=caption)
    
    # Foydalanuvchiga xabar va bosh menyuni ko‘rsatish
    await message.answer("✅ Skrinshot qabul qilindi! Hisobingizga **20 000 so‘m** qo‘shildi.", reply_markup=main_keyboard)

# **💰 Hisobim**
@dp.message(F.text == "💰 Hisobim")
async def check_balance(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = {"balance": 0}

    balance = user_balances[user_id]["balance"]
    await message.answer(f"💰 Hisobingiz: {balance:,} so‘m.")

# **🏦 Pul yechib olish**
@dp.message(F.text == "🏦 Pul yechib olish")
async def withdraw_command(message: types.Message):
    user_id = message.from_user.id
    balance = user_balances.get(user_id, {}).get("balance", 0)

    if balance >= 20000:
        await message.answer("💳 Kartangiz yoki telefon raqamingizni yuboring (8600 yoki +998 bilan boshlansin).")
    else:
        await message.answer("❌ Hisobingizda mablag‘ yetarli emas.")

# **Pul yechib olish uchun kartani yuborish**
@dp.message(F.text.regexp(r'^\d{4} \d{4} \d{4} \d{4}$') | F.text.regexp(r'^\+998\d{9}$'))
async def process_withdrawal_request(message: types.Message):
    user_id = message.from_user.id
    card_number = message.text  

    await bot.send_message(
        ADMIN_ID, f"💸 **Yangi pul yechish so‘rovi!**\n👤 @{message.from_user.username}\n💳 `{card_number}`\nTasdiqlash kerak!"
    )
    await message.answer("✅ So‘rovingiz qabul qilindi! Hisobingiz tez orada to‘ldiriladi.")

# **🎉 Konkurs**
@dp.message(F.text == "🎉 Konkurs")
async def contest_info(message: types.Message):
    await message.answer("🎊 Hozirda hech qanday konkurs yo‘q. Tez orada yangiliklar bo‘ladi!")

# **👥 Referal**
@dp.message(F.text == "👥 Referal")
async def referral_info(message: types.Message):
    user_id = message.from_user.id
    referral_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    await message.answer(f"👥 Do‘stlaringizni taklif qiling!\n🔗 Sizning referal havolangiz: {referral_link}")

# **ℹ️ Qo‘llanma**
@dp.message(F.text == "ℹ️ Qo‘llanma")
async def guide_info(message: types.Message):
    await message.answer("📘 Ovoz berish bo‘yicha qo‘llanma:\n\n"
                         "🔗 https://youtu.be/zENspAgKwu8?si=z3WHzdW6-I_pwi1n")

# **🔙 Orqaga**
@dp.message(F.text == "🔙 Orqaga")
async def go_back(message: types.Message):
    await message.answer("🔄 Bosh menyuga qaytdingiz.", reply_markup=main_keyboard)

# **Botni ishga tushirish**
async def main():
    print("Bot ishga tushdi!")
    await get_bot_username()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
