from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

API_ID = 31050502              
API_HASH = "30899f260555ef9e1ae8725cce3d540c"      
BOT_TOKEN = "8627446273:AAH4hsKW2SMyBlxzPmSdQIrdJauP1tPoO7U"    

# يوزرنيم القناة العامة
CHANNEL_USERNAME = "sbtbh"         
ARCHIVE_CHANNEL_ID = -1003818172414   

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def check_channel_membership(client, user_id):
    try:
        # فحص حالة العضو في القناة
        member = await client.get_chat_member(CHANNEL_USERNAME, user_id)
        print(f"حالة المستخدم {user_id} في القناة هي: {member.status}")
        
        if member.status in ["creator", "administrator", "member", "restricted"]:
            return True
        return False
    except Exception as e:
        # نطبع الخطأ بالكامل حتى نعرف هل هو بسبب صلاحيات البوت بالقناة أم شي ثاني
        print(f"خطأ دقيق في فحص الاشتراك: {e}")
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
    
    await message.reply("أهلاً بك! تم التحقق من اشتراكك بنجاح ✅.\nاختر المقطع الذي تريد مشاهدته من القائمة أدناه 👇", reply_markup=keyboard)

@app.on_callback_query(filters.regex("check_channel"))
async def verify_channel(client, callback_query):
    user_id = callback_query.from_user.id
    in_channel = await check_channel_membership(client, user_id)
    
    if not in_channel:
        await callback_query.answer("عذراً، لم تقم بالاشتراك في القناة أو لم يتم رصد اشتراكك بعد! ❌", show_alert=True)
        return

    await callback_query.answer("تم التحقق بنجاح! 🎉", show_alert=False)
    try:
        await callback_query.message.delete()
    except:
        pass
    await show_videos_menu(callback_query.message)

@app.on_message(filters.text & filters.private)
async def send_selected_video(client, message):
    text = message.text
    
    if text == "/start":
        return

    videos_messages = {
        "🎥 المقطع الأول": 3,   
        "🎥 المقطع الثاني": 2,   
        "🎥 المقطع الثالث": 4,   
        "🎥 المقطع الرابع": 5,   
        "🎥 المقطع الخامس": 6    
    }
    
    if text in videos_messages:
        user_id = message.from_user.id
        in_channel = await check_channel_membership(client, user_id)
        if not in_channel:
            await message.reply(f"عذراً، يجب عليك الاشتراك في القناة (@{CHANNEL_USERNAME}) أولاً لاستخدام البوت 📢")
            return

        msg_id = videos_messages[text]
        try:
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=ARCHIVE_CHANNEL_ID,
                message_id=msg_id,
                caption=f"تفضل، هذا هو {text} 🎬"
            )
        except Exception as e:
            await message.reply(f"عذراً، حدث خطأ أثناء إرسال المقطع.")
            print(f"خطأ نسخ الرسالة: {e}")

print("البوت جاهز مع نظام الفحص المطور...")
app.run()
