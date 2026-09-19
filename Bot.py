from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# بياناتك الأساسية مع التوكن الجديد
API_ID = 31050502              
API_HASH = "30899f260555ef9e1ae8725cce3d540c"      
BOT_TOKEN = "8627446273:AAH4hsKW2SMyBlxzPmSdQIrdJauP1tPoO7U"    

CHANNEL_ID = -1001697421048           
CHANNEL_USERNAME = "sbtbh"            

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# دالة فحص القناة الإجباري
async def check_channel_membership(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"خطأ قناة: {e}")
        return False
    return False

# أمر البدء /start
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

# قائمة الفيديوهات
async def show_videos_menu(message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 المقطع الأول", callback_data="vid_1")],
        [InlineKeyboardButton("🎥 المقطع الثاني", callback_data="vid_2")],
        [InlineKeyboardButton("🎥 المقطع الثالث", callback_data="vid_3")],
        [InlineKeyboardButton("🎥 المقطع الرابع", callback_data="vid_4")],
        [InlineKeyboardButton("🎥 المقطع الخامس", callback_data="vid_5")]
    ])
    
    if hasattr(message, "reply_text"):
        await message.reply_text("أهلاً بك! تم التحقق من اشتراكك بنجاح ✅.\nاختر المقطع الذي تريد مشاهدته:", reply_markup=keyboard)
    else:
        await message.edit_text("أهلاً بك! تم التحقق من اشتراكك بنجاح ✅.\nاختر المقطع الذي تريد مشاهدته:", reply_markup=keyboard)

# زر التحقق من القناة
@app.on_callback_query(filters.regex("check_channel"))
async def verify_channel(client, callback_query):
    user_id = callback_query.from_user.id
    in_channel = await check_channel_membership(client, user_id)
    
    if in_channel:
        await callback_query.answer("تم التحقق من القناة بنجاح! 🎉", show_alert=False)
        await callback_query.message.delete()
        await show_videos_menu(callback_query.message)
    else:
        await callback_query.answer("عذراً، لم يتم رصد اشتراكك بالقناة بعد!", show_alert=True)

# إرسال الفيديوهات
@app.on_callback_query(filters.regex(r"^vid_\d$"))
async def send_selected_video(client, callback_query):
    user_id = callback_query.from_user.id
    in_channel = await check_channel_membership(client, user_id)
    
    if not in_channel:
        await callback_query.answer("يجب عليك الاشتراك في القناة أولاً!", show_alert=True)
        return

    video_num = callback_query.data.split("_")[1]
    
    videos_file_ids = {
        "1": "AAMCAgADGQEDk6aoaq6369d6nq0JG2N-eqFFcMGjDMEAAgymAAJoBHFJhJrud-OGaigBAAdtAAM9BA",
        "2": "AAMCAgADGQEDk6apaq6362yaB3ZD3XzbBDFDRofaOYkAAsCpAAJggnhJ6P49nAMFTWEBAAdtAAM9BA",
        "3": "AAMCAgADGQEDk6araq6365Y1_LyTmuhJ9suB06Zv5ogAAsKpAAJggnhJ62j7onf695oBAAdtAAM9BA",
        "4": "AAMCAgADGQEDk6asaq636xTh_JmpIKLjurF84MQoNy8AAi2lAAJoBHFJB8TXrbRglYwBAAdtAAM9BA",
        "5": "AAMCAgADGQEDk6aqaq6362TI5AgcCHCODvTQlFcEiDIAAsGpAAJggnhJCxgAAaPG0RHFAQAHbQADPQQ"
    }
    
    file_id = videos_file_ids.get(video_num)
    await callback_query.message.reply_video(video=file_id, caption=f"تفضل، هذا هو المقطع رقم {video_num} 🎬")
    await callback_query.answer()

print("البوت يعمل بالتوكن الجديد وبشكل تامة...")
app.run()
    
