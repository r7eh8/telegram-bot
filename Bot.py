from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

API_ID = 31050502              
API_HASH = "30899f260555ef9e1ae8725cce3d540c"      
BOT_TOKEN = "8627446273:AAH4hsKW2SMyBlxzPmSdQIrdJauP1tPoO7U"    

CHANNEL_ID = -1001697421048        # الآيدي الرقمي للقناة
CHANNEL_USERNAME = "sbtbh"         # معرف القناة

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# دالة فحص اشتراك دقيقة وآمنة
async def check_channel_membership(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
    except Exception as e:
        print(f"خطأ في فحص الاشتراك: {e}")
        # إذا حدث خطأ في الفحص، نعتبره غير مشترك أو نسمح حسب الحاجة، لكن الأصح إرجاع False لضمان دقة القناة
        return False
    return False

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    in_channel = await check_channel_membership(client, user_id)
    
    if not in_channel:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("اشترك في القناة 📢", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("تحقق من اشتراك القناة ✅", callback_data="check_channel")]
        ])
        await message.reply(
            f"عذراً، يجب عليك الاشتراك في القناة (@{CHANNEL_USERNAME}) أولاً لتتمكن من استخدام البوت.\n\nبعد الاشتراك اضغط على زر التحقق أدناه 👇",
            reply_markup=keyboard
        )
        return

    await show_videos_menu(message)

async def show_videos_menu(message):
    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("🎥 المقطع الأول"), KeyboardButton("🎥 المقطع الثاني")],
        [KeyboardButton("🎥 المقطع الثالث"), KeyboardButton("🎥 المقطع الرابع")],
        [KeyboardButton("🎥 المقطع الخامس")]
    ], resize_keyboard=True)
    
    if hasattr(message, "reply_text"):
        await message.reply_text("أهلاً بك! تم التحقق من اشتراكك بنجاح ✅.\nاختر المقطع الذي تريد مشاهدته من القائمة أدناه 👇", reply_markup=keyboard)
    else:
        await message.reply("أهلاً بك! تم التحقق من اشتراكك بنجاح ✅.\nاختر المقطع الذي تريد مشاهدته من القائمة أدناه 👇", reply_markup=keyboard)

@app.on_callback_query(filters.regex("check_channel"))
async def verify_channel(client, callback_query):
    user_id = callback_query.from_user.id
    in_channel = await check_channel_membership(client, user_id)
    
    if in_channel:
        await callback_query.answer("تم التحقق من اشتراكك بنجاح! 🎉", show_alert=False)
        try:
            await callback_query.message.delete()
        except:
            pass
        await show_videos_menu(callback_query.message)
    else:
        await callback_query.answer("عذراً، لم يتم رصد اشتراكك بالقناة بعد! يرجى الاشتراك أولاً.", show_alert=True)

# استقبال الضغط على أزرار القائمة السفلى وإرسال الفيديوهات
@app.on_message(filters.text & filters.private)
async def send_selected_video(client, message):
    text = message.text
    user_id = message.from_user.id
    
    # فحص الاشتراك أيضاً قبل إرسال الفيديو لضمان عدم تخطي القناة
    in_channel = await check_channel_membership(client, user_id)
    if not in_channel:
        await message.reply("عذراً، يجب عليك الاشتراك في القناة أولاً لتتمكن من استلام المقاطع! اضغط /start من جديد.")
        return

    videos_data = {
        "🎥 المقطع الأول": "AAMCAgADGQEDk6aoaq6369d6nq0JG2N-eqFFcMGjDMEAAgymAAJoBHFJhJrud-OGaigBAAdtAAM9BA",
        "🎥 المقطع الثاني": "AAMCAgADGQEDk6apaq6362yaB3ZD3XzbBDFDRofaOYkAAsCpAAJggnhJ6P49nAMFTWEBAAdtAAM9BA",
        "🎥 المقطع الثالث": "AAMCAgADGQEDk6araq6365Y1_LyTmuhJ9suB06Zv5ogAAsKpAAJggnhJ62j7onf695oBAAdtAAM9BA",
        "🎥 المقطع الرابع": "AAMCAgADGQEDk6asaq636xTh_JmpIKLjurF84MQoNy8AAi2lAAJoBHFJB8TXrbRglYwBAAdtAAM9BA",
        "🎥 المقطع الخامس": "AAMCAgADGQEDk6aqaq6362TI5AgcCHCODvTQlFcEiDIAAsGpAAJggnhJCxgAAaPG0RHFAQAHbQADPQQ"
    }
    
    if text in videos_data:
        file_id = videos_data[text]
        try:
            await message.reply_video(video=file_id, caption=f"تفضل، هذا هو {text} 🎬")
        except Exception as e:
            await message.reply(f"عذراً، حدث خطأ أثناء إرسال المقطع. تأكد من صحة معرف الفيديو (file_id).")
            print(f"خطأ إرسال الفيديو: {e}")

print("البوت يعمل بكامل الكفاءة وحل المشاكل...")
app.run()
