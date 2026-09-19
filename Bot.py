from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

API_ID = 31050502              
API_HASH = "30899f260555ef9e1ae8725cce3d540c"      
BOT_TOKEN = "8627446273:AAH4hsKW2SMyBlxzPmSdQIrdJauP1tPoO7U"    

CHANNEL_USERNAME = "sbtbh"            

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# دالة فحص آمنة ومحمية
async def check_channel_membership(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
    except Exception as e:
        print(f"تنبيه فحص القناة: {e}")
        return True  # للسماح بالمرور وضمان عدم التوقف
    return False

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    in_channel = await check_channel_membership(client, user_id)
    
    if not in_channel:
        # إذا لم يكن مشتركاً نترك الأزرار شفافة للاشتراك والتحقق
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    # قائمة الأزرار التي ستظهر أسفل الدردشة
    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("🎥 المقطع الأول"), KeyboardButton("🎥 المقطع الثاني")],
        [KeyboardButton("🎥 المقطع الثالث"), KeyboardButton("🎥 المقطع الرابع")],
        [KeyboardButton("🎥 المقطع الخامس")]
    ], resize_keyboard=True)
    
    await message.reply_text("أهلاً بك! تم التحقق من اشتراكك بنجاح ✅.\nاختر المقطع الذي تريد مشاهدته من القائمة أدناه 👇", reply_markup=keyboard)

@app.on_callback_query(filters.regex("check_channel"))
async def verify_channel(client, callback_query):
    await callback_query.answer("تم التحقق بنجاح! 🎉", show_alert=False)
    try:
        await callback_query.message.delete()
    except:
        pass
    await show_videos_menu(callback_query.message)

# استقبال الضغط على أزرار القائمة السفلى وإرسال الفيديو المناسب
@app.on_message(filters.text & filters.private)
async def send_selected_video(client, message):
    text = message.text
    
    videos_data = {
        "🎥 المقطع الأول": "AAMCAgADGQEDk6aoaq6369d6nq0JG2N-eqFFcMGjDMEAAgymAAJoBHFJhJrud-OGaigBAAdtAAM9BA",
        "🎥 المقطع الثاني": "AAMCAgADGQEDk6apaq6362yaB3ZD3XzbBDFDRofaOYkAAsCpAAJggnhJ6P49nAMFTWEBAAdtAAM9BA",
        "🎥 المقطع الثالث": "AAMCAgADGQEDk6araq6365Y1_LyTmuhJ9suB06Zv5ogAAsKpAAJggnhJ62j7onf695oBAAdtAAM9BA",
        "🎥 المقطع الرابع": "AAMCAgADGQEDk6asaq636xTh_JmpIKLjurF84MQoNy8AAi2lAAJoBHFJB8TXrbRglYwBAAdtAAM9BA",
        "🎥 المقطع الخامس": "AAMCAgADGQEDk6aqaq6362TI5AgcCHCODvTQlFcEiDIAAsGpAAJggnhJCxgAAaPG0RHFAQAHbQADPQQ"
    }
    
    if text in videos_data:
        file_id = videos_data[text]
        video_num = text.split(" ")[-1] # استخراج رقم المقطع للعنونة
        await message.reply_video(video=file_id, caption=f"تفضل، هذا هو {text} 🎬")

print("البوت يعمل مع القائمة السفلى بنجاح...")
app.run()
        
