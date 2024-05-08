from pyrogram import Client, filters
from g4f.models import gpt_4
from g4f import ChatCompletion
import tracemalloc
from time import sleep 

from pyrogram.errors  import FloodWait
from pyrogram.types import Message, ChatPermissions
from time import time
from datetime import datetime, timedelta

tracemalloc.start()
app = Client("my_account")

    
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type_command(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    text_to_be_printed = ""
    typing_symbol = "ㅤ"
    while text_to_be_printed != orig_text:
        try:
            msg.edit(text_to_be_printed + typing_symbol)
            sleep(0.05)
            
            text_to_be_printed = text_to_be_printed + text[0]
            text = text[1:]
            
            msg.edit(text_to_be_printed)
            sleep(0.05)
            
        except FloodWait as e:  
            sleep(e)


@app.on_message(filters.command("mute", prefixes="."))
async def mute_command_handler(client, message):
    # Проверяем, есть ли аргументы после команды /mute
    if len(message.command) < 3:
        await message.reply_text("Пожалуйста, укажите пользователя и время мута.")
        return

    # Получаем имя пользователя и время мута из аргументов команды
    username = message.command[1]
    
    mute_duration_minutes = int(message.command[2])  # Продолжительность мута в минутах

    try:
        chat_id = message.chat.id
        # Получаем объект пользователя по его имени
        user = await client.get_users(username)
        user_id = user.id
        # Вычисляем время окончания мута и выставляем разрешения 
        until_date = datetime.now() + timedelta(minutes=mute_duration_minutes)
        permissions = ChatPermissions()
        
        # Применяем мут к пользователю до указанного времени
        await client.restrict_chat_member(chat_id, user_id, until_date=until_date, permissions=permissions)
        
        await message.send_text(f"Пользователь {username} замучен на {mute_duration_minutes} минут.")
        
        
    except Exception as e:
        await message.reply_text(f"Ошибка: {str(e)}")


@app.on_message(filters.command("unmute", prefixes=".") & filters.me)
async def unmute_func(client, message):
    # Проверяем, есть ли в команде имя пользователя
    if len(message.command) < 2:
        await message.reply_text("Укажите имя пользователя через @")
        return

    # Получение имени пользователя из команды
    username = message.command[1]

    try:
        # Получение объекта участника чата
        chat_member = await Client.get_chat_member(message.chat.id, message.from_user.id, username)
        print(chat_member.user.username)
        if chat_member.can_send_messages is True:
            await message.reply_text("Пользователь не замучен.")
            return

        permission = ChatPermissions(
            can_send_messages=True, can_send_media_messages=True,
        )

        # Размут пользователя
        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=chat_member.user.id,
            permissions=permission
        )

        await message.reply_text(f"Пользователь {username} успешно размучен.")

    except Exception as e:
        await message.reply_text(f"Возникла ошибка: {e}")
        
        
@app.on_message(filters.command("ask_gpt", prefixes="."))
async def gpt(client, message):
    question =  message.text
    message_to_send = message.text.replace('.ask_gpt', ' ')
    
    start_timer = time()
    answer = await ChatCompletion.create_async(model=gpt_4,    
    messages=[{"role": "user", "content": question}])
    end_timer = time()
    
    if len(answer) >= 4096:
         with open("answer.txt", "w") as file:
            file.write(answer)
            await app.send_document(message.chat.id, file, file_caption="Ответ оказался слишком большим, и записан в файл")
            
    elif len(answer) < 4096:       
        await message.reply_text(f"Gpt-answer: {answer}")
        
    all_need_time = round(end_timer - start_timer, 2)
    print(f"Request generated in  {all_need_time}sec")         
        
        
print("UserBot Started")           
app.run()                                     