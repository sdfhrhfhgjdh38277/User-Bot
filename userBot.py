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
