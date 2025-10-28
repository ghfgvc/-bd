from pyrogram import Client, filters
from pyrogram.types import LabeledPrice
import asyncio
import os

API_ID = 12345678  # استبدل بـ api_id الحقيقي
API_HASH = "your_api_hash"  # استبدل بـ api_hash الحقيقي
BOT_TOKEN = "7908908306:AAHhnTN8s0XeYwtZBC5xCo-T46OvEU2nZsE"

app = Client("payment_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# معرف القناة الخاصة
PRIVATE_CHANNEL = "https://t.me/+xpxNfyk7N9JhZjA0"

# أمر بدء الشراء
@app.on_message(filters.command("شراء"))
async def buy_handler(client, message):
    await client.send_invoice(
        chat_id=message.chat.id,
        title="اشتراك يوم في قناة المحتوى",
        description="اشتراك لمدة 24 ساعة في القناة الخاصة",
        payload="movie_subscription",
        provider_token="TEST:12345",  # رمز دفع وهمي
        currency="USD",
        prices=[LabeledPrice("اشتراك يوم", 300 * 100)],  # 300 نجمة = 3.00 دولار
        start_parameter="movie_sub"
    )

# التحقق المسبق من الدفع
@app.on_pre_checkout_query()
async def pre_checkout(client, query):
    await query.answer(ok=True)

# بعد الدفع الناجح
@app.on_message(filters.successful_payment)
async def successful_payment(client, message):
    user_id = message.from_user.id
    payload = message.successful_payment.invoice_payload

    if payload == "movie_subscription":
        await message.reply("✅ تم الدفع بنجاح! سيتم إضافتك إلى القناة لمدة 24 ساعة.")
        try:
            await app.add_chat_members(chat_id=PRIVATE_CHANNEL, user_ids=[user_id])
            await asyncio.sleep(86400)  # 24 ساعة
            await app.ban_chat_member(chat_id=PRIVATE_CHANNEL, user_id=user_id)
            await app.unban_chat_member(chat_id=PRIVATE_CHANNEL, user_id=user_id)
        except Exception as e:
            await message.reply(f"حدث خطأ أثناء إضافة المستخدم: {e}")

app.run()
